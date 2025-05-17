package main

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"github.com/rabbitmq/amqp091-go" // RabbitMQ client
)

type RequestBody struct {
	Name string `json:"name"`
}

type ValidateBody struct {
	Name  string `json:"name"`
	Token string `json:"token"`
}

var (
	redisClient *redis.Client
	ctx         = context.Background()
	amqpConn    *amqp091.Connection
	amqpChannel *amqp091.Channel
)

const (
	requestQueueName  = "auth_request_queue"
	validateQueueName = "auth_validate_queue"
)

func init() {
	redisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})

	_, err := redisClient.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Could not connect to Redis: %v", err)
	}
	log.Println("Connected to Redis successfully!")

	// Initialize the RabbitMQ connection
	// Replace with your RabbitMQ connection details if necessary
	amqpConn, err = amqp091.Dial("amqp://guest:guest@localhost:5672/") // Default RabbitMQ address and credentials
	if err != nil {
		log.Fatalf("Could not connect to RabbitMQ: %v", err)
	}
	log.Println("Connected to RabbitMQ successfully!")

	// Create a channel
	amqpChannel, err = amqpConn.Channel()
	if err != nil {
		log.Fatalf("Could not create RabbitMQ channel: %v", err)
	}

	// Declare the queues (idempotent - creates if they don't exist)
	_, err = amqpChannel.QueueDeclare(
		requestQueueName, // name
		true,             // durable
		false,            // delete when unused
		false,            // exclusive
		false,            // no-wait
		nil,              // arguments
	)
	if err != nil {
		log.Fatalf("Could not declare request queue: %v", err)
	}

	_, err = amqpChannel.QueueDeclare(
		validateQueueName, // name
		true,              // durable
		false,             // delete when unused
		false,             // exclusive
		false,             // no-wait
		nil,               // arguments
	)
	if err != nil {
		log.Fatalf("Could not declare validate queue: %v", err)
	}

	log.Println("RabbitMQ queues declared successfully!")
}

// handleRequestMessage processes messages from the request queue
func handleRequestMessage(d amqp091.Delivery) {
	log.Printf("Received a message from %s queue: %s", requestQueueName, d.Body)

	var reqBody RequestBody
	err := json.Unmarshal(d.Body, &reqBody)
	if err != nil {
		log.Printf("Error decoding request message: %v", err)
		d.Nack(false, false) // Negative acknowledgment, don't requeue
		return
	}

	if reqBody.Name == "" {
		log.Println("Request message missing name")
		d.Nack(false, false)
		return
	}

	// Generate a unique API token
	token := uuid.New().String()

	// Store the name-token mapping in Redis with a 24-hour expiration
	err = redisClient.Set(ctx, reqBody.Name, token, 24*time.Hour).Err()
	if err != nil {
		log.Printf("Error storing token in Redis for %s: %v", reqBody.Name, err)
		d.Nack(false, true) // Negative acknowledgment, requeue for retry
		return
	}

	log.Printf("Generated token for name: %s. Token: %s", reqBody.Name, token)

	// Acknowledge the message has been processed successfully
	d.Ack(false)

	// TODO: Implement sending a response back via a reply queue if needed
	// For now, we just log the generated token.
}

// handleValidateMessage processes messages from the validate queue
func handleValidateMessage(d amqp091.Delivery) {
	log.Printf("Received a message from %s queue: %s", validateQueueName, d.Body)

	var reqBody ValidateBody
	err := json.Unmarshal(d.Body, &reqBody)
	if err != nil {
		log.Printf("Error decoding validate message: %v", err)
		d.Nack(false, false) // Negative acknowledgment, don't requeue
		return
	}

	if reqBody.Name == "" || reqBody.Token == "" {
		log.Println("Validate message missing name or token")
		d.Nack(false, false)
		return
	}

	// Retrieve the token for the given name from Redis
	storedToken, err := redisClient.Get(ctx, reqBody.Name).Result()

	// Handle Redis errors
	if err == redis.Nil {
		log.Printf("Validation failed for name: %s - Name not found", reqBody.Name)
		// TODO: Indicate validation failure, perhaps via a reply queue
	} else if err != nil {
		log.Printf("Error retrieving token from Redis for %s: %v", reqBody.Name, err)
		d.Nack(false, true) // Negative acknowledgment, requeue for retry
		return
	} else {
		// Compare the provided token with the stored token
		if storedToken == reqBody.Token {
			log.Printf("Validation successful for name: %s", reqBody.Name)
			// TODO: Indicate validation success, perhaps via a reply queue
		} else {
			log.Printf("Validation failed for name: %s - Invalid token", reqBody.Name)
			// TODO: Indicate validation failure, perhaps via a reply queue
		}
	}

	// Acknowledge the message has been processed successfully
	d.Ack(false)
}

func main() {
	defer amqpConn.Close()
	defer amqpChannel.Close()

	// Start consuming from the request queue
	requestMsgs, err := amqpChannel.Consume(
		requestQueueName, // queue
		"",               // consumer
		false,            // auto-ack (set to false for manual acknowledgment)
		false,            // exclusive
		false,            // no-local
		false,            // no-wait
		nil,              // args
	)
	if err != nil {
		log.Fatalf("Could not start consuming from request queue: %v", err)
	}

	// Start consuming from the validate queue
	validateMsgs, err := amqpChannel.Consume(
		validateQueueName, // queue
		"",                // consumer
		false,             // auto-ack (set to false for manual acknowledgment)
		false,             // exclusive
		false,             // no-local
		false,             // no-wait
		nil,               // args
	)
	if err != nil {
		log.Fatalf("Could not start consuming from validate queue: %v", err)
	}

	log.Println("Auth service is listening for messages on RabbitMQ queues...")

	// Use goroutines to process messages concurrently
	go func() {
		for d := range requestMsgs {
			handleRequestMessage(d)
		}
	}()

	go func() {
		for d := range validateMsgs {
			handleValidateMessage(d)
		}
	}()

	// Keep the main function running to listen for messages
	select {}
}

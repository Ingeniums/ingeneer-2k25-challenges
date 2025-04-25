package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type Data struct {
    Data []string
}

type MessageResponse struct {
    Message string
}

func response(w http.ResponseWriter, status int, body any) int {
    w.Header().Set("Content-Type", "application/json")
    if body != nil {
        ret, err := json.Marshal(body)
        if err != nil {
            w.WriteHeader(http.StatusInternalServerError)
            return http.StatusInternalServerError
        }
        w.Write(ret)
    }

    w.WriteHeader(status)
    return status
}
type Step struct {
    Name string
    Dependencies []string
}

var Steps []Step = []Step{
}

func main() {
    req := []string{"val1", "val2", "val3"}

    http.HandleFunc("/submit", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodPost {
            response(w, http.StatusBadRequest, MessageResponse{
                Message: "Only Post method allowed on this route",
            })
            return
        }

        log.Printf("%s: /submit", r.Method)
        var inputs Data
        json.NewDecoder(r.Body).Decode(&inputs)

        satisfied := true
        for i := range len(req) {
            if i >= len(inputs.Data) {
                satisfied = false
                break
            }

            found := false
            for _, input := range inputs.Data {
                if input == req[i] {
                    found = true
                    break
                }
            }
            if !found {
                satisfied = false
                break
            }
        }

        if !satisfied {
            response(w, http.StatusBadRequest, MessageResponse{
                Message: "Some requirements are missing.",
            })
            return
        }

        response(w, http.StatusOK, MessageResponse{
            Message: "Success",
        })
    })

    log.Println("Server listening on port 8080...")
    http.ListenAndServe(":8080", nil)
}

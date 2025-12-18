club_credentials=(
  "contact@parisbball.fr"
  "contact@strasbourg.fr"
  "contact@boulogne.fr"
)
player_credentials=(
  "player1@ryze.fr"
  "player2@ryze.fr"
  "player3@ryze.fr"
)
agent_credentials=(
  "agent1@france.fr"
  "agent2@france.fr"
  "agent3@france.fr"
)
admin_credentials=(
  "admin@ryze.fr"
)

password="password123"

url="https://ryze-tm2z.onrender.com/login"

log_file="login_test_output.log"
> "$log_file"

for email in "${club_credentials[@]}"; do
  echo "Testing club: $email" | tee -a "$log_file"
  curl -s -X POST "$url" \
    -H "Content-Type: application/json" \
    -d '{"user_type":"club","email":"'$email'","password":"'$password'"}' \
    | tee -a "$log_file"
  echo -e "\n---\n" | tee -a "$log_file"
done

for email in "${player_credentials[@]}"; do
  echo "Testing player: $email" | tee -a "$log_file"
  curl -s -X POST "$url" \
    -H "Content-Type: application/json" \
    -d '{"user_type":"player","email":"'$email'","password":"'$password'"}' \
    | tee -a "$log_file"
  echo -e "\n---\n" | tee -a "$log_file"
done

for email in "${agent_credentials[@]}"; do
  echo "Testing agent: $email" | tee -a "$log_file"
  curl -s -X POST "$url" \
    -H "Content-Type: application/json" \
    -d '{"user_type":"agent","email":"'$email'","password":"'$password'"}' \
    | tee -a "$log_file"
  echo -e "\n---\n" | tee -a "$log_file"
done

for email in "${admin_credentials[@]}"; do
  echo "Testing admin: $email" | tee -a "$log_file"
  curl -s -X POST "$url" \
    -H "Content-Type: application/json" \
    -d '{"user_type":"admin","email":"'$email'","password":"'$password'"}' \
    | tee -a "$log_file"
  echo -e "\n---\n" | tee -a "$log_file"
done

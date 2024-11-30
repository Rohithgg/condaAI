import requests

base_url = "http://localhost:8080"

def get_server_health():
    response = requests.get(f'{base_url}/health')
    return response.json()

def post_completion(context, user_input):
    prompt = f"{context}\n User: {user_input}\n Assistant"
    data = {
        'temperature': 0.8,
        'prompt': prompt,
        'top_k': 200, #to control test generation if any problem  change to 35.
        'top_p':0.95,
        'n_predict': 200,
        'stop': ["<s>", "Assistant:", "User"]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{base_url}/completion', json = data, headers = headers)
    if response.status_code == 200:
        return response.json()['content'].strip()
    else:
        return "Error processing your request"
def update_context(context, user_input, assistant_response):
    return f"{context}\nUser: {user_input}\nAssistant: {assistant_response}"
def main():
    print("welcome to blogger AI")
    context = "you are a professional blogger. The blog post should include an introduction, main body, and conclusion. The conclusion should invite readers to leave a comment. The main body should be split into at least 4 different subsections."
    health = get_server_health()
    print('Server Health:', health)

    if health.get('status') == 'ok':
        while True:
            user_input = input("Enter a prompt or type 'exit' to quit: ")
            if user_input.lower() == 'exit':
                break
            assistant_response = post_completion(context, user_input)
            print('Assistant:', assistant_response)

            context = update_context(context, user_input, assistant_response)
    else:
        print("Server is not ready for requests.")

if __name__ == "__main__":
    main()
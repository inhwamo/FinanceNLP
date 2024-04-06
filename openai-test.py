from openai import OpenAI

def get_user_input(prompt):
    return input(prompt)

def main():
    client = OpenAI()

    # Prompt user for system content
    default_system_content = "You are a helpful assistant."
    system_content = get_user_input(f"Enter system content, e.g. 'You are a poetic assistant, skilled in explaining complex programming concepts with creative flair' \nor press Enter to use the default ('{default_system_content}')\n: ")

    if not system_content:
      system_content = default_system_content 
    user_content = get_user_input("Enter user content, e.g. 'Compose a poem that explains the concept of recursion in programming.'\n: ")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )

    print(completion.choices[0].message.content.replace('\n', ' '))    

if __name__ == "__main__":
    main()

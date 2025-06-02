from OpenAIChatHelper import ChatCompletionEndPoint
from OpenAIChatHelper.message import (
    SubstitutionDict,
    MessageList,
    DevSysUserMessage,
    AssistantMessage,
    TextContent,
)

###################### Create a ChatCompletionEndPoint instance ######################

chatbot = ChatCompletionEndPoint(
    default_model="gpt-4o"
)  # Refer to OpenAI docs for supported models
print("-" * 20 + "Finished Initialization" + "-" * 20)

####################### Example Usage of ChatCompletionEndPoint ######################

# Create a message list to hold the conversation
message_list = (
    MessageList()
)  # see OpenAIChatHelper/message/MessageList.py for more details/functionality

# Add a system prompt to define the assistant’s behavior
message_list.add_message(
    DevSysUserMessage(
        "system",
        TextContent(
            "You are an AI chatbot that helps people classify the sentiment of their words. "
            "Respond with 'Positive', 'Negative', 'Neutral', 'Mixed', or 'Unknown', followed by a brief explanation."
        ),  # see OpenAIChatHelper/message/Contents.py for more details/functionality
    )  # see OpenAIChatHelper/message/Message.py for more details/functionality
)

# Add an initial user message
message_list.add_message(
    DevSysUserMessage(
        "user",
        TextContent("I hate this restaurant!"),
    )
)

print("Current Message List:")
print(message_list)  # directly printable
print("-" * 40)

# Generate 2 model completions with temperature 1.0
responses, meta = chatbot.completions(
    message_list, temperature=1.0, n=2
)  # also accepts all kwargs supported by OpenAI API

# meta is the original ChatCompletion object, which contains metadata about the request

# Display the completions
for i, response in enumerate(responses, 1):  # responses is a list of Message
    print(f"Response {i}:")
    print(response)  # response is a Message object, which can be printed directly
    for content in response:
        # content is a Content object, could be TextContent, ImageContent, etc.
        if isinstance(content, TextContent):
            print(f"Text Content: {content.text}")
        # see OpenAIChatHelper/message/Contents.py for more details/functionality and other content types
print("-" * 40)

# Add the first assistant response to the message list for continued conversation
message_list.add_message(responses[0])

# Optionally, you could also add it like this:
# message_list.add_message(
#     AssistantMessage(TextContent(responses[0][0].text))
# )

# Add another user message
message_list.add_message(
    DevSysUserMessage(
        "user",
        TextContent("I love this place!"),
    )
)

print("Updated Message List:")
print(message_list)
print("-" * 40)

# Get another model response
new_responses, meta = chatbot.completions(message_list, temperature=1.0, n=1)

print("Response to the updated message list:")
print(new_responses[0])  # Print the new response
print("-" * 40)


######### Example of using SubstitutionDict to replace variables in messages #########


# sometimes you want to replace "variables" in messages and do not want to modify the original message list

# Remove the last 3 messages (2 user messages and 1 assistant reply) from the list.
# We retain only the original system prompt.
message_list.pop_messages(3)

print("Message List after popping last 3 messages (so there's only the system prompt):")
print(message_list)
print("-" * 40)

# Add a message with a placeholder (user's review) to demonstrate variable substitution
message_list.add_message(
    DevSysUserMessage(
        "user",
        TextContent("Review:\n{user's review}"),
    )
)

# Create a dictionary of substitutions
substitution_dict = SubstitutionDict()
substitution_dict["user's review"] = "I love this place!"

print("Message List before substitution:")
print(message_list)
print("-" * 40)

# Preview what the message list looks like after applying substitutions
print("Substituting variables in the message list...")
print(
    message_list.to_dict(substitution_dict)
)  # Note: this returns a substituted version; it does not mutate the original list; you do not need to call this method unless you want to see the substituted version
print("-" * 40)

# Use message list with subtitution_dict to get a response
responses, meta = chatbot.completions(
    message_list, substitution_dict=substitution_dict, temperature=1.0, n=1
)

print("Response after substitution:")
for response in responses:
    print(response)  # Print the response after substitution
print("-" * 40)


############### Other tools and utilities ###############

# Create a new message list for a different task
message_list = MessageList()

# Add a user's prompt to the message list
message_list.add_message(
    DevSysUserMessage(
        "user",
        TextContent("List some reasons why I might like a restaurant."),
    )
)

# Get a response from the chatbot
responses, meta = chatbot.completions(message_list, temperature=1.0, n=1)

response = responses[0][0]

if isinstance(response, TextContent):
    # the response is likely a list of reasons
    print("Response:")
    print(response)

    # split the response into an ordered list, remove markdown formatting if needed; see OpenAIChatHelper/message/Contents.py for more details
    splitted_list = response.split_ordered_list()  # a list of strings
    print("Splitted List:")
    for item in splitted_list:
        print(f"- {item}")

    # remove markdown formatting; see OpenAIChatHelper/message/Contents.py for more details
    cleaned_text = response.remove_markdown()
    print("Cleaned Text:")
    print(cleaned_text)

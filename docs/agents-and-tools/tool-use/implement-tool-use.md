# How to implement tool use

## Choosing a model

Generally, use Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4.5, Claude Sonnet 4, Claude Sonnet 3.7, Claude Sonnet 3.5 ([deprecated](/en/docs/about-claude/model-deprecations)) or Claude Opus 3 ([deprecated](/en/docs/about-claude/model-deprecations)) for complex tools and ambiguous queries; they handle multiple tools better and seek clarification when needed.

Use Claude Haiku 3.5 or Claude Haiku 3 for straightforward tools, but note they may infer missing parameters.

<Tip>
  If using Claude Sonnet 3.7 with tool use and extended thinking, refer to our guide [here](/en/docs/build-with-claude/extended-thinking) for more information.
</Tip>

## Specifying client tools

Client tools (both Anthropic-defined and user-defined) are specified in the `tools` top-level parameter of the API request. Each tool definition includes:

| Parameter      | Description                                                                                         |
| :------------- | :-------------------------------------------------------------------------------------------------- |
| `name`         | The name of the tool. Must match the regex `^[a-zA-Z0-9_-]{1,64}$`.                                 |
| `description`  | A detailed plaintext description of what the tool does, when it should be used, and how it behaves. |
| `input_schema` | A [JSON Schema](https://json-schema.org/) object defining the expected parameters for the tool.     |

<Accordion title="Example simple tool definition">
  ```JSON JSON theme={null}
  {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
        }
      },
      "required": ["location"]
    }
  }
  ```

  This tool, named `get_weather`, expects an input object with a required `location` string and an optional `unit` string that must be either "celsius" or "fahrenheit".
</Accordion>

### Tool use system prompt

When you call the Claude API with the `tools` parameter, we construct a special system prompt from the tool definitions, tool configuration, and any user-specified system prompt. The constructed prompt is designed to instruct the model to use the specified tool(s) and provide the necessary context for the tool to operate properly:

```
In this environment you have access to a set of tools you can use to answer the user's question.
{{ FORMATTING INSTRUCTIONS }}
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}
{{ USER SYSTEM PROMPT }}
{{ TOOL CONFIGURATION }}
```

### Best practices for tool definitions

To get the best performance out of Claude when using tools, follow these guidelines:

* **Provide extremely detailed descriptions.** This is by far the most important factor in tool performance. Your descriptions should explain every detail about the tool, including:
  * What the tool does
  * When it should be used (and when it shouldn't)
  * What each parameter means and how it affects the tool's behavior
  * Any important caveats or limitations, such as what information the tool does not return if the tool name is unclear. The more context you can give Claude about your tools, the better it will be at deciding when and how to use them. Aim for at least 3-4 sentences per tool description, more if the tool is complex.
* **Prioritize descriptions over examples.** While you can include examples of how to use a tool in its description or in the accompanying prompt, this is less important than having a clear and comprehensive explanation of the tool's purpose and parameters. Only add examples after you've fully fleshed out the description.

<AccordionGroup>
  <Accordion title="Example of a good tool description">
    ```JSON JSON theme={null}
    {
      "name": "get_stock_price",
      "description": "Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {
            "type": "string",
            "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
          }
        },
        "required": ["ticker"]
      }
    }
    ```
  </Accordion>

  <Accordion title="Example poor tool description">
    ```JSON JSON theme={null}
    {
      "name": "get_stock_price",
      "description": "Gets the stock price for a ticker.",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {
            "type": "string"
          }
        },
        "required": ["ticker"]
      }
    }
    ```
  </Accordion>
</AccordionGroup>

The good description clearly explains what the tool does, when to use it, what data it returns, and what the `ticker` parameter means. The poor description is too brief and leaves Claude with many open questions about the tool's behavior and usage.

## Controlling Claude's output

### Forcing tool use

In some cases, you may want Claude to use a specific tool to answer the user's question, even if Claude thinks it can provide an answer without using a tool. You can do this by specifying the tool in the `tool_choice` field like so:

```
tool_choice = {"type": "tool", "name": "get_weather"}
```

When working with the tool\_choice parameter, we have four possible options:

* `auto` allows Claude to decide whether to call any provided tools or not. This is the default value when `tools` are provided.
* `any` tells Claude that it must use one of the provided tools, but doesn't force a particular tool.
* `tool` allows us to force Claude to always use a particular tool.
* `none` prevents Claude from using any tools. This is the default value when no `tools` are provided.

<Note>
  When using [prompt caching](/en/docs/build-with-claude/prompt-caching#what-invalidates-the-cache), changes to the `tool_choice` parameter will invalidate cached message blocks. Tool definitions and system prompts remain cached, but message content must be reprocessed.
</Note>

This diagram illustrates how each option works:

<Frame>
  <img src="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=fb88b9fa0da23fc231e4fece253f4406" data-og-width="1920" width="1920" data-og-height="1080" height="1080" data-path="images/tool_choice.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=280&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=11a4cfd7ab7815ea14c21e0948d060d4 280w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=560&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=c889c279adce34f1fa479bc722b3fe6f 560w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=840&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=e16651305d256ded74250f1c0dadb622 840w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=1100&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=a99b0dd3b603051efdf9536ba9307a34 1100w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=1650&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=5045888f298f7261d3ae2e1466e54027 1650w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/tool_choice.png?w=2500&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=8a9c615a15610a949a2dad3aaa8113b8 2500w" />
</Frame>

Note that when you have `tool_choice` as `any` or `tool`, we will prefill the assistant message to force a tool to be used. This means that the models will not emit a natural language response or explanation before `tool_use` content blocks, even if explicitly asked to do so.

<Note>
  When using [extended thinking](/en/docs/build-with-claude/extended-thinking) with tool use, `tool_choice: {"type": "any"}` and `tool_choice: {"type": "tool", "name": "..."}` are not supported and will result in an error. Only `tool_choice: {"type": "auto"}` (the default) and `tool_choice: {"type": "none"}` are compatible with extended thinking.
</Note>

Our testing has shown that this should not reduce performance. If you would like the model to provide natural language context or explanations while still requesting that the model use a specific tool, you can use `{"type": "auto"}` for `tool_choice` (the default) and add explicit instructions in a `user` message. For example: `What's the weather like in London? Use the get_weather tool in your response.`

### JSON output

Tools do not necessarily need to be client functions — you can use tools anytime you want the model to return JSON output that follows a provided schema. For example, you might use a `record_summary` tool with a particular schema. See [Tool use with Claude](/en/docs/agents-and-tools/tool-use/overview) for a full working example.

### Model responses with tools

When using tools, Claude will often comment on what it's doing or respond naturally to the user before invoking tools.

For example, given the prompt "What's the weather like in San Francisco right now, and what time is it there?", Claude might respond with:

```JSON JSON theme={null}
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll help you check the current weather and time in San Francisco."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": {"location": "San Francisco, CA"}
    }
  ]
}
```

This natural response style helps users understand what Claude is doing and creates a more conversational interaction. You can guide the style and content of these responses through your system prompts and by providing `<examples>` in your prompts.

It's important to note that Claude may use various phrasings and approaches when explaining its actions. Your code should treat these responses like any other assistant-generated text, and not rely on specific formatting conventions.

### Parallel tool use

By default, Claude may use multiple tools to answer a user query. You can disable this behavior by:

* Setting `disable_parallel_tool_use=true` when tool\_choice type is `auto`, which ensures that Claude uses **at most one** tool
* Setting `disable_parallel_tool_use=true` when tool\_choice type is `any` or `tool`, which ensures that Claude uses **exactly one** tool

<AccordionGroup>
  <Accordion title="Complete parallel tool use example">
    Here's a complete example showing how to properly format parallel tool calls in the message history:

    <CodeGroup>
      ```python Python theme={null}
      import anthropic

      client = anthropic.Anthropic()

      # Define tools
      tools = [
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA"
                      }
                  },
                  "required": ["location"]
              }
          },
          {
              "name": "get_time",
              "description": "Get the current time in a given timezone",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "timezone": {
                          "type": "string",
                          "description": "The timezone, e.g. America/New_York"
                      }
                  },
                  "required": ["timezone"]
              }
          }
      ]

      # Initial request
      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          tools=tools,
          messages=[
              {
                  "role": "user",
                  "content": "What's the weather in SF and NYC, and what time is it there?"
              }
          ]
      )

      # Claude's response with parallel tool calls
      print("Claude wants to use tools:", response.stop_reason == "tool_use")
      print("Number of tool calls:", len([c for c in response.content if c.type == "tool_use"]))

      # Build the conversation with tool results
      messages = [
          {
              "role": "user",
              "content": "What's the weather in SF and NYC, and what time is it there?"
          },
          {
              "role": "assistant",
              "content": response.content  # Contains multiple tool_use blocks
          },
          {
              "role": "user",
              "content": [
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_01",  # Must match the ID from tool_use
                      "content": "San Francisco: 68°F, partly cloudy"
                  },
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_02",
                      "content": "New York: 45°F, clear skies"
                  },
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_03",
                      "content": "San Francisco time: 2:30 PM PST"
                  },
                  {
                      "type": "tool_result",
                      "tool_use_id": "toolu_04",
                      "content": "New York time: 5:30 PM EST"
                  }
              ]
          }
      ]

      # Get final response
      final_response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          tools=tools,
          messages=messages
      )

      print(final_response.content[0].text)
      ```

      ```typescript TypeScript theme={null}
      import { Anthropic } from '@anthropic-ai/sdk';

      const anthropic = new Anthropic();

      // Define tools
      const tools = [
        {
          name: "get_weather",
          description: "Get the current weather in a given location",
          input_schema: {
            type: "object",
            properties: {
              location: {
                type: "string",
                description: "The city and state, e.g. San Francisco, CA"
              }
            },
            required: ["location"]
          }
        },
        {
          name: "get_time",
          description: "Get the current time in a given timezone",
          input_schema: {
            type: "object",
            properties: {
              timezone: {
                type: "string",
                description: "The timezone, e.g. America/New_York"
              }
            },
            required: ["timezone"]
          }
        }
      ];

      // Initial request
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        tools: tools,
        messages: [
          {
            role: "user",
            content: "What's the weather in SF and NYC, and what time is it there?"
          }
        ]
      });

      // Build conversation with tool results
      const messages = [
        {
          role: "user",
          content: "What's the weather in SF and NYC, and what time is it there?"
        },
        {
          role: "assistant",
          content: response.content  // Contains multiple tool_use blocks
        },
        {
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: "toolu_01",  // Must match the ID from tool_use
              content: "San Francisco: 68°F, partly cloudy"
            },
            {
              type: "tool_result",
              tool_use_id: "toolu_02",
              content: "New York: 45°F, clear skies"
            },
            {
              type: "tool_result",
              tool_use_id: "toolu_03",
              content: "San Francisco time: 2:30 PM PST"
            },
            {
              type: "tool_result",
              tool_use_id: "toolu_04",
              content: "New York time: 5:30 PM EST"
            }
          ]
        }
      ];

      // Get final response
      const finalResponse = await anthropic.messages.create({
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        tools: tools,
        messages: messages
      });

      console.log(finalResponse.content[0].text);
      ```
    </CodeGroup>

    The assistant message with parallel tool calls would look like this:

    ```json  theme={null}
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "I'll check the weather and time for both San Francisco and New York City."
        },
        {
          "type": "tool_use",
          "id": "toolu_01",
          "name": "get_weather",
          "input": {"location": "San Francisco, CA"}
        },
        {
          "type": "tool_use",
          "id": "toolu_02",
          "name": "get_weather",
          "input": {"location": "New York, NY"}
        },
        {
          "type": "tool_use",
          "id": "toolu_03",
          "name": "get_time",
          "input": {"timezone": "America/Los_Angeles"}
        },
        {
          "type": "tool_use",
          "id": "toolu_04",
          "name": "get_time",
          "input": {"timezone": "America/New_York"}
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Complete test script for parallel tools">
    Here's a complete, runnable script to test and verify parallel tool calls are working correctly:

    <CodeGroup>
      ```python Python theme={null}
      #!/usr/bin/env python3
      """Test script to verify parallel tool calls with the Claude API"""

      import os
      from anthropic import Anthropic

      # Initialize client
      client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

      # Define tools
      tools = [
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA"
                      }
                  },
                  "required": ["location"]
              }
          },
          {
              "name": "get_time",
              "description": "Get the current time in a given timezone",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "timezone": {
                          "type": "string",
                          "description": "The timezone, e.g. America/New_York"
                      }
                  },
                  "required": ["timezone"]
              }
          }
      ]

      # Test conversation with parallel tool calls
      messages = [
          {
              "role": "user",
              "content": "What's the weather in SF and NYC, and what time is it there?"
          }
      ]

      # Make initial request
      print("Requesting parallel tool calls...")
      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          messages=messages,
          tools=tools
      )

      # Check for parallel tool calls
      tool_uses = [block for block in response.content if block.type == "tool_use"]
      print(f"\n✓ Claude made {len(tool_uses)} tool calls")

      if len(tool_uses) > 1:
          print("✓ Parallel tool calls detected!")
          for tool in tool_uses:
              print(f"  - {tool.name}: {tool.input}")
      else:
          print("✗ No parallel tool calls detected")

      # Simulate tool execution and format results correctly
      tool_results = []
      for tool_use in tool_uses:
          if tool_use.name == "get_weather":
              if "San Francisco" in str(tool_use.input):
                  result = "San Francisco: 68°F, partly cloudy"
              else:
                  result = "New York: 45°F, clear skies"
          else:  # get_time
              if "Los_Angeles" in str(tool_use.input):
                  result = "2:30 PM PST"
              else:
                  result = "5:30 PM EST"
          
          tool_results.append({
              "type": "tool_result",
              "tool_use_id": tool_use.id,
              "content": result
          })

      # Continue conversation with tool results
      messages.extend([
          {"role": "assistant", "content": response.content},
          {"role": "user", "content": tool_results}  # All results in one message!
      ])

      # Get final response
      print("\nGetting final response...")
      final_response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          messages=messages,
          tools=tools
      )

      print(f"\nClaude's response:\n{final_response.content[0].text}")

      # Verify formatting
      print("\n--- Verification ---")
      print(f"✓ Tool results sent in single user message: {len(tool_results)} results")
      print("✓ No text before tool results in content array")
      print("✓ Conversation formatted correctly for future parallel tool use")
      ```

      ```typescript TypeScript theme={null}
      #!/usr/bin/env node
      // Test script to verify parallel tool calls with the Claude API

      import { Anthropic } from '@anthropic-ai/sdk';

      const anthropic = new Anthropic({
        apiKey: process.env.ANTHROPIC_API_KEY
      });

      // Define tools
      const tools = [
        {
          name: "get_weather",
          description: "Get the current weather in a given location",
          input_schema: {
            type: "object",
            properties: {
              location: {
                type: "string",
                description: "The city and state, e.g. San Francisco, CA"
              }
            },
            required: ["location"]
          }
        },
        {
          name: "get_time",
          description: "Get the current time in a given timezone",
          input_schema: {
            type: "object",
            properties: {
              timezone: {
                type: "string",
                description: "The timezone, e.g. America/New_York"
              }
            },
            required: ["timezone"]
          }
        }
      ];

      async function testParallelTools() {
        // Make initial request
        console.log("Requesting parallel tool calls...");
        const response = await anthropic.messages.create({
          model: "claude-sonnet-4-5",
          max_tokens: 1024,
          messages: [{
            role: "user",
            content: "What's the weather in SF and NYC, and what time is it there?"
          }],
          tools: tools
        });

        // Check for parallel tool calls
        const toolUses = response.content.filter(block => block.type === "tool_use");
        console.log(`\n✓ Claude made ${toolUses.length} tool calls`);

        if (toolUses.length > 1) {
          console.log("✓ Parallel tool calls detected!");
          toolUses.forEach(tool => {
            console.log(`  - ${tool.name}: ${JSON.stringify(tool.input)}`);
          });
        } else {
          console.log("✗ No parallel tool calls detected");
        }

        // Simulate tool execution and format results correctly
        const toolResults = toolUses.map(toolUse => {
          let result;
          if (toolUse.name === "get_weather") {
            result = toolUse.input.location.includes("San Francisco") 
              ? "San Francisco: 68°F, partly cloudy"
              : "New York: 45°F, clear skies";
          } else {
            result = toolUse.input.timezone.includes("Los_Angeles")
              ? "2:30 PM PST"
              : "5:30 PM EST";
          }
          
          return {
            type: "tool_result",
            tool_use_id: toolUse.id,
            content: result
          };
        });

        // Get final response with correct formatting
        console.log("\nGetting final response...");
        const finalResponse = await anthropic.messages.create({
          model: "claude-sonnet-4-5",
          max_tokens: 1024,
          messages: [
            { role: "user", content: "What's the weather in SF and NYC, and what time is it there?" },
            { role: "assistant", content: response.content },
            { role: "user", content: toolResults }  // All results in one message!
          ],
          tools: tools
        });

        console.log(`\nClaude's response:\n${finalResponse.content[0].text}`);

        // Verify formatting
        console.log("\n--- Verification ---");
        console.log(`✓ Tool results sent in single user message: ${toolResults.length} results`);
        console.log("✓ No text before tool results in content array");
        console.log("✓ Conversation formatted correctly for future parallel tool use");
      }

      testParallelTools().catch(console.error);
      ```
    </CodeGroup>

    This script demonstrates:

    * How to properly format parallel tool calls and results
    * How to verify that parallel calls are being made
    * The correct message structure that encourages future parallel tool use
    * Common mistakes to avoid (like text before tool results)

    Run this script to test your implementation and ensure Claude is making parallel tool calls effectively.
  </Accordion>
</AccordionGroup>

#### Maximizing parallel tool use

While Claude 4 models have excellent parallel tool use capabilities by default, you can increase the likelihood of parallel tool execution across all models with targeted prompting:

<AccordionGroup>
  <Accordion title="System prompts for parallel tool use">
    For Claude 4 models (Opus 4.1, Opus 4, and Sonnet 4), add this to your system prompt:

    ```text  theme={null}
    For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
    ```

    For even stronger parallel tool use (recommended if the default isn't sufficient), use:

    ```text  theme={null}
    <use_parallel_tool_calls>
    For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. When running multiple read-only commands like `ls` or `list_dir`, always run all of the commands in parallel. Err on the side of maximizing parallel tool calls rather than running too many tools sequentially.
    </use_parallel_tool_calls>
    ```
  </Accordion>

  <Accordion title="User message prompting">
    You can also encourage parallel tool use within specific user messages:

    ```python  theme={null}
    # Instead of:
    "What's the weather in Paris? Also check London."

    # Use:
    "Check the weather in Paris and London simultaneously."

    # Or be explicit:
    "Please use parallel tool calls to get the weather for Paris, London, and Tokyo at the same time."
    ```
  </Accordion>
</AccordionGroup>

<Warning>
  **Parallel tool use with Claude Sonnet 3.7**

  Claude Sonnet 3.7 may be less likely to make make parallel tool calls in a response, even when you have not set `disable_parallel_tool_use`. To work around this, we recommend enabling [token-efficient tool use](/en/docs/agents-and-tools/tool-use/token-efficient-tool-use), which helps encourage Claude to use parallel tools. This beta feature also reduces latency and saves an average of 14% in output tokens.

  If you prefer not to opt into the token-efficient tool use beta, you can also introduce a "batch tool" that can act as a meta-tool to wrap invocations to other tools simultaneously. We find that if this tool is present, the model will use it to simultaneously call multiple tools in parallel for you.

  See [this example](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/parallel_tools_claude_3_7_sonnet.ipynb) in our cookbook for how to use this workaround.
</Warning>

## Handling tool use and tool result content blocks

Claude's response differs based on whether it uses a client or server tool.

### Handling results from client tools

The response will have a `stop_reason` of `tool_use` and one or more `tool_use` content blocks that include:

* `id`: A unique identifier for this particular tool use block. This will be used to match up the tool results later.
* `name`: The name of the tool being used.
* `input`: An object containing the input being passed to the tool, conforming to the tool's `input_schema`.

<Accordion title="Example API response with a `tool_use` content block">
  ```JSON JSON theme={null}
  {
    "id": "msg_01Aq9w938a90dw8q",
    "model": "claude-sonnet-4-5",
    "stop_reason": "tool_use",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "I'll check the current weather in San Francisco for you."
      },
      {
        "type": "tool_use",
        "id": "toolu_01A09q90qw90lq917835lq9",
        "name": "get_weather",
        "input": {"location": "San Francisco, CA", "unit": "celsius"}
      }
    ]
  }
  ```
</Accordion>

When you receive a tool use response for a client tool, you should:

1. Extract the `name`, `id`, and `input` from the `tool_use` block.
2. Run the actual tool in your codebase corresponding to that tool name, passing in the tool `input`.
3. Continue the conversation by sending a new message with the `role` of `user`, and a `content` block containing the `tool_result` type and the following information:
   * `tool_use_id`: The `id` of the tool use request this is a result for.
   * `content`: The result of the tool, as a string (e.g. `"content": "15 degrees"`), a list of nested content blocks (e.g. `"content": [{"type": "text", "text": "15 degrees"}]`), or a list of document blocks (e.g. `"content": ["type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "15 degrees"}]`). These content blocks can use the `text`, `image`, or `document` types.
   * `is_error` (optional): Set to `true` if the tool execution resulted in an error.

<Note>
  **Important formatting requirements**:

  * Tool result blocks must immediately follow their corresponding tool use blocks in the message history. You cannot include any messages between the assistant's tool use message and the user's tool result message.
  * In the user message containing tool results, the tool\_result blocks must come FIRST in the content array. Any text must come AFTER all tool results.

  For example, this will cause a 400 error:

  ```json  theme={null}
  {"role": "user", "content": [
    {"type": "text", "text": "Here are the results:"},  // ❌ Text before tool_result
    {"type": "tool_result", "tool_use_id": "toolu_01", ...}
  ]}
  ```

  This is correct:

  ```json  theme={null}
  {"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": "toolu_01", ...},
    {"type": "text", "text": "What should I do next?"}  // ✅ Text after tool_result
  ]}
  ```

  If you receive an error like "tool\_use ids were found without tool\_result blocks immediately after", check that your tool results are formatted correctly.
</Note>

<AccordionGroup>
  <Accordion title="Example of successful tool result">
    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "15 degrees"
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Example of tool result with images">
    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": [
            {"type": "text", "text": "15 degrees"},
            {
              "type": "image",
              "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "/9j/4AAQSkZJRg...",
              }
            }
          ]
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Example of empty tool result">
    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
        }
      ]
    }
    ```
  </Accordion>

  <Accordion title="Example of tool result with documents">
    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": [
            {"type": "text", "text": "The weather is"},
            {
              "type": "document",
              "source": {
                "type": "text",
                "media_type": "text/plain",
                "data": "15 degrees"
              }
            }
          ]
        }
      ]
    }
    ```
  </Accordion>
</AccordionGroup>

After receiving the tool result, Claude will use that information to continue generating a response to the original user prompt.

### Handling results from server tools

Claude executes the tool internally and incorporates the results directly into its response without requiring additional user interaction.

<Tip>
  **Differences from other APIs**

  Unlike APIs that separate tool use or use special roles like `tool` or `function`, the Claude API integrates tools directly into the `user` and `assistant` message structure.

  Messages contain arrays of `text`, `image`, `tool_use`, and `tool_result` blocks. `user` messages include client content and `tool_result`, while `assistant` messages contain AI-generated content and `tool_use`.
</Tip>

### Handling the `max_tokens` stop reason

If Claude's [response is cut off due to hitting the `max_tokens` limit](/en/api/handling-stop-reasons#max-tokens), and the truncated response contains an incomplete tool use block, you'll need to retry the request with a higher `max_tokens` value to get the full tool use.

<CodeGroup>
  ```python Python theme={null}
  # Check if response was truncated during tool use
  if response.stop_reason == "max_tokens":
      # Check if the last content block is an incomplete tool_use
      last_block = response.content[-1]
      if last_block.type == "tool_use":
          # Send the request with higher max_tokens
          response = client.messages.create(
              model="claude-sonnet-4-5",
              max_tokens=4096,  # Increased limit
              messages=messages,
              tools=tools
          )
  ```

  ```typescript TypeScript theme={null}
  // Check if response was truncated during tool use
  if (response.stop_reason === "max_tokens") {
    // Check if the last content block is an incomplete tool_use
    const lastBlock = response.content[response.content.length - 1];
    if (lastBlock.type === "tool_use") {
      // Send the request with higher max_tokens
      response = await anthropic.messages.create({
        model: "claude-sonnet-4-5",
        max_tokens: 4096, // Increased limit
        messages: messages,
        tools: tools
      });
    }
  }
  ```
</CodeGroup>

#### Handling the `pause_turn` stop reason

When using server tools like web search, the API may return a `pause_turn` stop reason, indicating that the API has paused a long-running turn.

Here's how to handle the `pause_turn` stop reason:

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Initial request with web search
  response = client.messages.create(
      model="claude-3-7-sonnet-latest",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Search for comprehensive information about quantum computing breakthroughs in 2025"
          }
      ],
      tools=[{
          "type": "web_search_20250305",
          "name": "web_search",
          "max_uses": 10
      }]
  )

  # Check if the response has pause_turn stop reason
  if response.stop_reason == "pause_turn":
      # Continue the conversation with the paused content
      messages = [
          {"role": "user", "content": "Search for comprehensive information about quantum computing breakthroughs in 2025"},
          {"role": "assistant", "content": response.content}
      ]
      
      # Send the continuation request
      continuation = client.messages.create(
          model="claude-3-7-sonnet-latest",
          max_tokens=1024,
          messages=messages,
          tools=[{
              "type": "web_search_20250305",
              "name": "web_search",
              "max_uses": 10
          }]
      )
      
      print(continuation)
  else:
      print(response)
  ```

  ```typescript TypeScript theme={null}
  import { Anthropic } from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  // Initial request with web search
  const response = await anthropic.messages.create({
    model: "claude-3-7-sonnet-latest",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Search for comprehensive information about quantum computing breakthroughs in 2025"
      }
    ],
    tools: [{
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 10
    }]
  });

  // Check if the response has pause_turn stop reason
  if (response.stop_reason === "pause_turn") {
    // Continue the conversation with the paused content
    const messages = [
      { role: "user", content: "Search for comprehensive information about quantum computing breakthroughs in 2025" },
      { role: "assistant", content: response.content }
    ];
    
    // Send the continuation request
    const continuation = await anthropic.messages.create({
      model: "claude-3-7-sonnet-latest",
      max_tokens: 1024,
      messages: messages,
      tools: [{
        type: "web_search_20250305",
        name: "web_search",
        max_uses: 10
      }]
    });
    
    console.log(continuation);
  } else {
    console.log(response);
  }
  ```
</CodeGroup>

When handling `pause_turn`:

* **Continue the conversation**: Pass the paused response back as-is in a subsequent request to let Claude continue its turn
* **Modify if needed**: You can optionally modify the content before continuing if you want to interrupt or redirect the conversation
* **Preserve tool state**: Include the same tools in the continuation request to maintain functionality

## Troubleshooting errors

There are a few different types of errors that can occur when using tools with Claude:

<AccordionGroup>
  <Accordion title="Tool execution error">
    If the tool itself throws an error during execution (e.g. a network error when fetching weather data), you can return the error message in the `content` along with `"is_error": true`:

    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "ConnectionError: the weather service API is not available (HTTP 500)",
          "is_error": true
        }
      ]
    }
    ```

    Claude will then incorporate this error into its response to the user, e.g. "I'm sorry, I was unable to retrieve the current weather because the weather service API is not available. Please try again later."
  </Accordion>

  <Accordion title="Invalid tool name">
    If Claude's attempted use of a tool is invalid (e.g. missing required parameters), it usually means that the there wasn't enough information for Claude to use the tool correctly. Your best bet during development is to try the request again with more-detailed `description` values in your tool definitions.

    However, you can also continue the conversation forward with a `tool_result` that indicates the error, and Claude will try to use the tool again with the missing information filled in:

    ```JSON JSON theme={null}
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
          "content": "Error: Missing required 'location' parameter",
          "is_error": true
        }
      ]
    }
    ```

    If a tool request is invalid or missing parameters, Claude will retry 2-3 times with corrections before apologizing to the user.
  </Accordion>

  <Accordion title="<search_quality_reflection> tags">
    To prevent Claude from reflecting on search quality with \<search\_quality\_reflection> tags, add "Do not reflect on the quality of the returned search results in your response" to your prompt.
  </Accordion>

  <Accordion title="Server tool errors">
    When server tools encounter errors (e.g., network issues with Web Search), Claude will transparently handle these errors and attempt to provide an alternative response or explanation to the user. Unlike client tools, you do not need to handle `is_error` results for server tools.

    For web search specifically, possible error codes include:

    * `too_many_requests`: Rate limit exceeded
    * `invalid_input`: Invalid search query parameter
    * `max_uses_exceeded`: Maximum web search tool uses exceeded
    * `query_too_long`: Query exceeds maximum length
    * `unavailable`: An internal error occurred
  </Accordion>

  <Accordion title="Parallel tool calls not working">
    If Claude isn't making parallel tool calls when expected, check these common issues:

    **1. Incorrect tool result formatting**

    The most common issue is formatting tool results incorrectly in the conversation history. This "teaches" Claude to avoid parallel calls.

    Specifically for parallel tool use:

    * ❌ **Wrong**: Sending separate user messages for each tool result
    * ✅ **Correct**: All tool results must be in a single user message

    ```json  theme={null}
    // ❌ This reduces parallel tool use
    [
      {"role": "assistant", "content": [tool_use_1, tool_use_2]},
      {"role": "user", "content": [tool_result_1]},
      {"role": "user", "content": [tool_result_2]}  // Separate message
    ]

    // ✅ This maintains parallel tool use
    [
      {"role": "assistant", "content": [tool_use_1, tool_use_2]},
      {"role": "user", "content": [tool_result_1, tool_result_2]}  // Single message
    ]
    ```

    See the [general formatting requirements above](#handling-tool-use-and-tool-result-content-blocks) for other formatting rules.

    **2. Weak prompting**

    Default prompting may not be sufficient. Use stronger language:

    ```text  theme={null}
    <use_parallel_tool_calls>
    For maximum efficiency, whenever you perform multiple independent operations, 
    invoke all relevant tools simultaneously rather than sequentially. 
    Prioritize calling tools in parallel whenever possible.
    </use_parallel_tool_calls>
    ```

    **3. Measuring parallel tool usage**

    To verify parallel tool calls are working:

    ```python  theme={null}
    # Calculate average tools per tool-calling message
    tool_call_messages = [msg for msg in messages if any(
        block.type == "tool_use" for block in msg.content
    )]
    total_tool_calls = sum(
        len([b for b in msg.content if b.type == "tool_use"]) 
        for msg in tool_call_messages
    )
    avg_tools_per_message = total_tool_calls / len(tool_call_messages)
    print(f"Average tools per message: {avg_tools_per_message}")
    # Should be > 1.0 if parallel calls are working
    ```

    **4. Model-specific behavior**

    * Claude Opus 4.1, Opus 4, and Sonnet 4: Excel at parallel tool use with minimal prompting
    * Claude Sonnet 3.7: May need stronger prompting or [token-efficient tool use](/en/docs/agents-and-tools/tool-use/token-efficient-tool-use)
    * Claude Haiku: Less likely to use parallel tools without explicit prompting
  </Accordion>
</AccordionGroup>

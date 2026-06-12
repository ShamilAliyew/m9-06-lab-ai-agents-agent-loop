![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Your First Agent

## Overview

You've built the tool-call loop by hand. Now you hand the wheel to the model. In this lab you build a single **agent** with **Google ADK**: you give it instructions, a couple of tools, and a goal — and it runs the **reason → act → observe** loop *on its own*, deciding which tools to call and when it's done. Your job shifts from driving the loop to **designing** the agent and then watching it work.

The goal you set needs more than one step, so you'll see the agent plan and chain tool calls without you scripting them.

## Learning Goals

- Define an ADK agent with instructions, tools, and a session
- Hand the agent a multi-step goal and let it run the loop itself
- Read the agent's trace — its reasoning and tool calls — to see how it got there

## Setup

Fork, clone, branch. Reuse your Gemini key; ADK uses `GOOGLE_API_KEY`.

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your-free-gemini-key"
```

> Keep tasks small — the free tier has rate limits, and an agent makes several model calls per run.

You're given `orders.json` again. (ADK is comfortable as a plain script, but a notebook works too.)

> **No starter code — you build it from scratch.** There's no template in this repo; create your own working file(s) and write the code yourself. This close to the end of the bootcamp, scaffolding your own project is part of the exercise.

## Your Task

**Build one ADK agent that solves a multi-step goal with its tools.**

1. Define **two tools** the agent can use:
   - `lookup_order(order_id)` — returns item, price, purchase date, warranty months from `orders.json`.
   - `calculate(expression)` — evaluates simple arithmetic.
2. Create a single ADK agent with:
   - **instructions** describing its job (a helpful orders assistant), when to use each tool, and an instruction to say so clearly if it can't find an order,
   - the **two tools**,
   - a **session** to hold the run.
3. Give it a goal that needs **multiple steps**, for example:
   > *"I'm thinking of buying two more of order A1001. What would those two cost, and is the original still under warranty?"*

   The agent should look up the order, calculate the cost of two, reason about the warranty, and answer — all on its own.
4. **Capture the trace**: show the agent's tool calls and reasoning steps, not just the final answer. The point is to *see the loop run itself*.

### Optional stretch

Give the agent a goal it **can't** complete (ask about order `A9999`). Confirm it uses the tool, gets "not found", and reports honestly rather than inventing an answer — your instructions should have prepared it for this.

## Submission

Commit your agent code and a captured run (trace + final answer) for the multi-step goal. Open a PR and paste the link.

## Quality Bar

- A single ADK agent with clear instructions, two tools, and a session
- The multi-step goal is solved by the agent's **own** tool choices, not a script you wrote
- The submitted run shows the agent's tool calls / reasoning, not just the answer
- No API key is committed

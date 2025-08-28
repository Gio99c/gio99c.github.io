---
layout: post
title: "A Practical Recipe for LLM Workflows"
date: 2025-08-13
categories: blog
excerpt: "A practical, no-nonsense recipe for LLM workflows: evaluate what matters, design simple systems, prompt with intent, and observe everything so you can ship something that actually works."
---

2025 is the hallmark year of LLM applications. Every practitioner and startup is focusing attention on the opportunity these systems offer. It almost seems that with a bit of tuning and the right instructions these models can carry out whatever task is thrown at them. However, the devil is in the details, and, as with every machine learning model, making this work at scale and in production environments is fairly challenging.

These models come with several challenges, and adapting them to your specific workflow requires both patience and clear-headed engineering. Many practitioners struggle when early outcomes feel underwhelming. To unlock real capability, you have to play by the system’s rules: understand limitations, respect how these models behave, and then leverage them deliberately. I’m not talking about re-deriving self-attention or rotary embeddings: those are one LLM call away. I’m talking about how to actually use these systems from a practical standpoint, even if you’re new. It’s just another tool; learn to play with it correctly and you can win the game.

I’ll share the lessons I’ve learned dealing with these systems and the practical moves I follow religiously every time I tackle a task with LLMs. In a nutshell, the key components to focus on are:

- **Evaluation**
- **System Design**
- **Prompting**
- **Observability**

It’s not important whether you use Claude or Llama: *the recipe is the same*. The parameters (temperature, model choice, prompt tweaks) are just small adjustments once the scaffolding is in place. Let’s get to the useful parts.

# Evaluation
Whatever your goal, before touching API keys or LLM calls, be crystal clear not only about what you want to achieve but, more importantly, **how you will measure it**. Evaluating LLM outputs is often the hardest part of scaling LLM workflows, but it’s no different from any other serious software: define KPIs and benchmark them to assess quality. The twist is that you have less control over behavior, and tiny changes can lead to very different outcomes. Regression tests and A/B tests are fundamental before making any change to your model.

I usually have two ways of assessing these models:

1. **Classification or information extraction evaluation**
If you just need to extract information, don’t reinvent the wheel. Use classic ML evaluation: confusion matrix, accuracy, F1—whatever fits the task.

2. **Outcome evaluation**
This is trickier and may require external validation (e.g., when you accept or request a code suggestion from Cursor) or deriving KPIs from outputs that are easily measured. If you have a reference outcome, compare the generation to your baseline and assess quality from there.

**Note:** even if evaluation is a big deal, it shouldn’t block you at the start. Know your metrics, but first get something working end-to-end. Once outcomes look promising, create a baseline and start evaluating against it.

# System Design
This is where your LLM architecture takes shape. It can be a simple chain of steps or a more complex graph, but the core is the same. I start with a small proof of concept (2–3 steps), then extend.

A common flow I use:

`Input → Information Extraction → Main Processing → Post-processing → Output`

- **Information extraction** is usually a fast step that pulls out signals from the input. For text, it might verify the presence of key terms or extract details for later. This is almost always classification/information retrieval, and it helps the main processing be more focused and lightweight. Depending on the task, this can branch the workflow’s path or change how it’s prompted. For example, classify the style of the input (teenager, adult, elder) and adjust the prompt accordingly (Gen-Z-ish, millennial, boomer).
- **Main processing** is where the magic happens and depends on your task: generating diff-style code from a request, reading information from an image, translating text, etc. This is where LLMs shine: tasks that would require too many brittle rules or an impractical domain-specific ML pipeline. My software engineering approach has shifted: I don’t start with agents by default. I use the *simplest solution that works*. When rule-based logic explodes into contradictions or the domain is too fuzzy, LLMs earn their keep. If classic CV can count lines in a grid, I’ll use it; when lines are occluded and messy, a vision LLM helps.

Whatever your application, treat it like real software:

- **Modular code**: think in atomic steps and tools, and follow the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). The less you repeat yourself and the more your tools are modular, the easier it is to maintain and scale.
- **Statefulness**: think through inputs/outputs and what must be stored across the workflow’s run.
- **Structure**: strictly define the data that flows through the system (types and requirements). Treat this like a schema or a strongly typed language. In Python, [Pydantic](https://docs.pydantic.dev/) is perfect for this.

I always start by defining the Pydantic models that will populate the system and the intermediate results. This *forces clarity* on what’s needed. Then every action is a simple function or node in the workflow. By thinking in functions and classes, it’s possible to structure even complex tasks—these systems still obey the same fundamentals of software engineering.

# Prompting
This is the main difference from classical coding or ML: instructions are natural language, with *inherent fuzziness*. The craft is trading off:

- **Context**: more task information vs. memory pressure
- **Specificity**: handling edge cases vs. keeping generality
- **Stability**: avoiding ambiguity and nondeterminism

Everything in the prompt affects the output. **Version prompts like code.** I decouple prompts from code and start by versioning with Git. When projects need more flexibility, I use a lightweight script (my “personal Git for prompts”) to check, store, diff across branches, merge, and track. There are dedicated tools—but I’ve consistently used [LangSmith](https://www.langchain.com/langsmith) for experiments and observability. Track prompts and keep a regression test baseline that you check whenever even a comma changes. Prompts shape output as much as data quality shapes classic ML—garbage in, garbage out.

**An example is worth a thousand tokens.** In almost every task, providing a few-shot prompt is extremely beneficial. The trick is to avoid over-biasing the model toward one modality while covering representative use cases. This is essential when you need a specific format, a precise task, or grounding information. Attaching data as images or small example files also helps when appropriate. The catch: don’t overfit the context and shrink the model’s effective capacity. For more on why examples matter, see "Examples are all you need" [here](https://opper.ai/blog/examples-are-all-you-need?utm_source=chatgpt.com).

# Observability
Understanding and following the call stack and the data flowing through intermediate steps is essential for LLM workflows. There are many tools for this. I use [LangSmith](https://www.langchain.com/langsmith); it integrates with most agent frameworks and lets you navigate LLM calls, inputs/outputs, token counts, model choices, and even cost.

Observing behavior helps debug weird edge cases and search historical runs. It’s a *no-brainer* to add this early. LangSmith is quick to set up (install, set env vars, open the dashboard), and for a low number of traces it’s free at the time of writing.

These are the absolute basics I suggest to every practitioner building an LLM workflow. Every flow is different, and applications are endless, but this is a broad recipe you can adapt whether you’re hacking for fun or shipping production. Enjoy!

## Further Reading

- A Recipe for Training Neural Networks — Andrej Karpathy: [link](https://karpathy.github.io/2019/04/25/recipe/)
- Examples are all you need (on the power of few-shot prompts): [link](https://opper.ai/blog/examples-are-all-you-need?utm_source=chatgpt.com)

## Useful Resources

- LangSmith (tracing, evals, observability): [link](https://www.langchain.com/langsmith)
- Cursor (LLM-native code editor, useful for outcome evaluation loops): [link](https://www.cursor.com)
- Pydantic (data validation and settings management): [link](https://docs.pydantic.dev/)
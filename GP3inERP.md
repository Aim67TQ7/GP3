# Why I Stopped Vectorizing My ERP Data and Built Knowledge Blocks Instead

*By Robert Clausing | n0v8v LLC*

---

Every AI consultant who walks into a manufacturing plant says the same thing.

"We'll pull your data, run it through embeddings, build a vector database, and your team can ask questions in plain English."

It sounds reasonable. It even works in demos. Then you go live and the thing hallucinates a lead time, inverts a quantity, or confidently answers a question about inventory using data that was accurate eight months ago.

I know because I tried it. I spent real time chasing vectorization inside a production Epicor environment before I figured out what was actually wrong.

---

## What Vectorization Does and Where It Breaks

Vectorization, or Retrieval-Augmented Generation (RAG), works like this: you take your documents or data exports, convert them into numerical representations called embeddings, and store them in a searchable index. When someone asks a question, the system finds the closest matching chunks and injects them into the AI's context as evidence.

The problem isn't the concept. The problem is what happens to manufacturing data when you treat it this way.

ERP data is not a document. It's a web of relationships, statuses, timestamps, and business logic that only means something in context. A job cost number means nothing without knowing the job status. A shipment record means nothing without the customer hold status. An open order means nothing without knowing whether the line items have been allocated.

When you chunk and embed that data, you lose the relationships. You get fragments. The AI does its best to fill the gaps with inference, and in manufacturing, inference is how you end up telling a customer their order ships Friday when it's actually sitting on a credit hold.

There's another problem: stale data. Vectorized indexes don't update in real time. Your AI is answering questions about a snapshot of your operation, not your operation.

---

## What I Found Instead

I stopped trying to teach the AI what my data contained and started teaching it how to read my data correctly.

The difference sounds subtle. It isn't.

Instead of converting Epicor records into embeddings, I built knowledge blocks. Structured packages that tell the AI exactly which data source to query, which fields matter, which values indicate a problem, and what business rules govern how that information should be interpreted. The AI then queries the live system and interprets the result through those rules.

No stale index. No hallucinated gap-filling. No chunking artifacts.

The knowledge blocks also handle what I call the Epicor viewing problem. Epicor is not dirty data. It's accurate data viewed incorrectly. Seven open tabs, six exported spreadsheets, a morning stand-up where half the information is already outdated by the time someone reads it. The data is there. The problem is the interface forcing you to reassemble it manually every single day.

Knowledge blocks set the rules for how that data gets assembled. Once. Then every query runs through those rules automatically.

---

## The Tribal Knowledge Problem

The bigger win came from something I didn't expect.

Every plant has people who know things the system doesn't. The planner who knows which customer always pushes back on lead times. The floor supervisor who knows machine three runs slow on Tuesday afternoons after maintenance. The sales rep who knows a particular account pays 45 days regardless of terms.

That knowledge lives in heads. When those people leave, it walks out the door with them.

Knowledge blocks capture that logic in a form the AI can apply consistently. Not as a document that gets searched, but as a rule that gets enforced on every response. The system doesn't guess at context. It applies the context it was given, and flags when the answer falls outside what it can verify.

That's how I got to single-day implementation at a new site. Not because the setup is simple, but because the framework already knows how to ask the right questions about a new environment and slot the answers into a working structure.

---

## What This Means for Your Operation

If you've already tried an AI tool on your ERP data and walked away disappointed, the issue probably wasn't the AI. It was the architecture underneath it.

Vectorization was built for documents. Knowledge blocks were built for operations.

The difference shows up in whether your team trusts the answer. In manufacturing, that trust is the whole product.

---

*Robert Clausing is the founder of n0v8v LLC, an AI advisory practice for mid-market manufacturers. He built and operates an Epicor intelligence layer inside a production environment for two years before taking the methodology to outside clients.*

*n0v8v LLC | [n0v8v.com](https://n0v8v.com)*

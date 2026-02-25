# Workflow: Research

## Description
Deep research on a given topic. Uses web search, web fetch, and memory to produce
a structured markdown report with findings, sources, and recommendations.

## Inputs
- `topic`: The research topic or question
- `depth`: Research depth — quick | standard | deep (default: standard)
- `output_path`: Where to write the report (default: /tmp/research-{timestamp}.md)

## Steps
1. **Memory check**
   - Search m2-memory for existing knowledge on topic
   - Note any prior decisions or warnings

2. **Web research**
   - Search web for top 5-10 sources
   - Fetch and extract key content from each
   - Cross-reference for consistency

3. **Synthesis**
   - Identify consensus findings
   - Flag contradictions or uncertainties
   - Extract actionable recommendations

4. **Report**
   - Write structured markdown to output_path
   - Sections: Summary, Key Findings, Sources, Recommendations, Caveats

## Outputs
- `report_path`: Path to the generated markdown report
- `summary`: 2-3 sentence summary of findings
- `source_count`: Number of sources consulted

## Guardrails
- Max 10 web fetches per run
- Skip paywalled content
- Flag low-confidence findings explicitly
- Max report length: 2000 tokens

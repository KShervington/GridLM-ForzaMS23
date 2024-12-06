This is how data is currently being aggregated for testing:

```txt
Retrieved 198 documents for segment 1
Average speeds: 65.07, 65.74, 66.40, 67.04, 67.67, 68.28, 68.88, 69.46, 70.02

Retrieved 205 documents for segment 2
Average speeds: 71.06, 71.60, 72.13, 72.63, 71.22, 65.13, 60.41, 56.60, 53.13

Retrieved 349 documents for segment 3
Average speeds: 48.90, 41.46, 36.54, 34.94, 33.55, 32.98, 34.48, 36.77, 38.79

Retrieved 296 documents for segment 4
Average speeds: 42.38, 44.66, 46.88, 48.96, 49.25, 44.19, 43.45, 43.54, 42.96

Retrieved 349 documents for segment 5
Average speeds: 37.06, 37.25, 36.55, 36.28, 37.10, 39.83, 41.71, 38.01, 36.57

Retrieved 352 documents for segment 6
Average speeds: 36.37, 38.26, 40.40, 41.13, 37.04, 37.47, 35.91, 34.55, 34.54

Retrieved 343 documents for segment 7
Average speeds: 36.28, 39.16, 42.41, 40.16, 38.03, 39.23, 37.67, 35.78, 36.66

Retrieved 399 documents for segment 8
Average speeds: 36.50, 34.65, 33.85, 31.81, 29.96, 29.39, 29.81, 32.17, 34.00

Retrieved 293 documents for segment 9
Average speeds: 38.63, 39.31, 40.73, 42.68, 45.16, 47.54, 49.79, 51.79, 53.10

Retrieved 220 documents for segment 10
Average speeds: 55.93, 57.19, 58.42, 59.61, 60.75, 61.83, 62.85, 63.82, 64.31
```

> See `src/langchain/get_llm_assessment.py` for how that is happening.

The above data is from the `reference_telemetries` collection in the mongoDB database. The goal is to get the same data for the `telemetries` collection, format both sets of data into a prompt template, and ask the LLM to compare performance.

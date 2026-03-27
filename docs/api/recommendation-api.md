# Recommendation API

The Recommendation API provides personalized book suggestions for students based on their academic and library usage profile.

## `get_book_recommendations()`
Returns personalized book recommendations grouped by the reason for suggestion.
- **Scoring Method**: Multi-factor scoring algorithm.
- **Output**:
  - `sections`: List of recommendation sections (e.g., "Program Core Essentials", "Based on Past Borrowing", "Popular Among Peers", "New Arrivals").
  - `total_recommendations`: Total count of suggested books across all sections.
- **Performance**:
  - **Caching**: Results are cached for 1 hour to ensure high performance.
  - **Relevance**: Scores are recalculate as new books are added or as student borrowing history evolves.

## Recommendation Section Metadata
Each section includes:
- `title`: Subjective title (e.g., "Program Core Essentials").
- `subtitle`: Descriptive explanation of why the books are suggested.
- `badge`: Brief label for UI display.
- `icon`: FontAwesome class for section visualization.
- `books`: List of up to 12 curated book entries.

The Recommendation API is key to driving engagement within the library.

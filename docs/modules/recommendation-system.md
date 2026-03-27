# Recommendation System

The Recommendation System module uses a multi-factor scoring algorithm to suggest the most relevant books to each student.

## Scoring Factors
The system calculates a score for each book based on five key factors:
- **Program Core (+5 points)**: The book is a core resource for the student's academic program.
- **Subject Match (+4 points)**: The book matches a subject the student is currently enrolled in.
- **Interest History (+2 points)**: The student has previously borrowed books from the same category.
- **Peer Popularity (+4 points)**: The book is frequently borrowed by other students in the same program.
- **New Arrival (+1 point)**: The book was recently added to the library (within the last 90 days).

## Recommendation Lists
Students receive personalized lists of up to 12 books per category, ensuring they discover resources that align with their studies and interests.

## Performance
- **Caching**: Recommendation scores are cached for 1 hour to ensure high performance while maintaining relevance.
- **Update Frequency**: Recommendations are refreshed as students borrow new items or as new books are added to the catalog.

This module enhances the learning experience by making resource discovery more intuitive and relevant.

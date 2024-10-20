# Book Search App

A Flask-based web application that allows users to search for books using the Google Books API. Users can search by title, author, ISBN, or publish year and view results in a table with sortable columns.

## Features

- **Search Books**: Search for books by title, author, ISBN, or publication year.
- **Sorting**: Sort search results by:
  - Book Title (ascending/descending)
  - Published Year (ascending/descending)
  - Description (ascending/descending)
- **Responsive Design**: The app is built using Bootstrap for a clean, responsive design.
- **Book Details**: Displays book information such as title, authors, ISBN, published year, description, and a thumbnail image of the book cover.

## Demo

This is a simple Flask web app that demonstrates how to query the Google Books API and display results in a sortable table.

## Usage

-Enter your search criteria (title, author, ISBN, or publication year) in the form fields.
-Click the "Search" button to query the Google Books API.
-View the results in the table below the search form.
-You can sort the results by clicking on the table headers for Title, Published Year, and Description. The arrow will indicate whether the sorting is ascending (▲) or descending (▼).

## API Integration
The app uses the Google Books API to fetch book data based on search criteria.

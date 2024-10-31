# IIIT-H Mess Menu Tracker

A web application to track daily mess menus at IIIT Hyderabad.

## About

This application displays the menu for different messes at IIIT Hyderabad, including:
- Yuktahaar
- Kadamba
- North Mess
- South Mess

## How to Update the Menu

1. Fork this repository
2. Navigate to `public/data/`
3. Update the respective Excel files:
   - `yuktahaar.xlsx`
   - `kadamba.xlsx`
   - `north.xlsx`
   - `south.xlsx`
4. Submit a Pull Request

### Excel File Format
The Excel files should follow this format:
- Rows 2-6: Breakfast items
- Rows 7-13: Lunch items
- Rows 14-15: Snacks items
- Rows 16-22: Dinner items
- Columns C-I represent days (Monday to Sunday)

## Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mess-menu-tracker.git

# Install dependencies
npm install

# Run the development server
npm run dev
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/UpdateMenu`)
3. Commit your changes (`git commit -m 'Updated menu for MM/YYYY'`)
4. Push to the branch (`git push origin feature/UpdateMenu`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or suggestions, please open an issue in the repository.

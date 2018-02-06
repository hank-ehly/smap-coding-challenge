# Implementation Notes

### Usage of Pandas library

I decided to use the `pandas` library to read the csv data into the Django database.

Granted the csv file is formatted correctly and duplicate records do not exist, 
the import logic can be reduced to 2 lines of code when paired with `bulk_create`.

```python
df = pd.read_csv('path/to/csv')
User.objects.bulk_create(  User(**vals) for vals in df.to_dict('records')  )
```

This approach has some drawbacks, including (but not limited to):
- High memory allocation (depends on size of CSV files)
- Duplicate record verification may be problematic

I think these drawbacks are relatively small considering the readability and simplicity of the implementation. In addition, `pandas` is frequently used in data processing, so there's a good chance it could be used elsewhere in the app later.

### Front End Code Organization

Front end assets (javascript / css) are located in `static/consumption`. Each page has its own dedicated javascript file. The `utils` file contains the `SCC` object, which is used by both views for various tasks like chart initialization, data parsing, and spinner-icon toggling.

All javascript is encapsulated to prevent cluttering of the global namespace. The `SCC` object is created from an anonymous function, so that the distinction between private and public properties & functions can be made (hint: `numberWithCommas` is only accessible from within `SCC`).

In future projects, I'd like to implement node-js build scripts using Gulp to take advantage of modern front-end development features like livereload, sass to css processing, autoprefixing, javascript uglification, and code encapsulation frameworks like RequireJS.

### Addition of ConsumptionRollup model

The `ConsumptionRollup` model is a rollup table that aggregates `Consumption` data by date (as opposed to datetime). At first I thought this wouldn't be needed; however, the chart in the summary view took upwards of 6~7 seconds to load without it. By implementing this model, I was able to cut the load time of the summary chart from 7 seconds to less than 1 second. 

`ConsumptionRollup` has one (tested!) method: `full_recalc`, which performs a full recalculation of all `Consumption` data. In the future, it would be best to implement more methods to handle incremental changes in the data without having to recalculate everything.

### Tests

I added the `tests` directory to house the different server-side tests. The `fixtures` directory includes a minature version of the project-root `data` csv data. To prevent stdout calls from the `import` command tests from blowing up the terminal, I replaced `stdout` with an instance of `StringIO`. In the future, I'd like to create seed files to handle test-data setup and make `setUpTestData` more DRY.

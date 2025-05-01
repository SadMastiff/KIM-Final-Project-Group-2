To run the following programs you will need:
-Python installed
-Beautiful Soup 4 installed
-Pandas installed 
-NumPy installed
-Matplotlib installed
-Requests installed

How each program operates:

"am_web_scrape.py":

- This program web scrapes 20 pages of listings of treadmills. 
- The following data is extracted: product name, rating (out of 5 stars), rating count, and price.
- All extracted listings are stored into a csv called "amazon_treadmills_clean.csv".
- *NOTE* If the scraper can not extract a certain rating, rating count, or price of a product the value will be 
   replace with "N/A"
- *NOTE* If desired to scrape another product, simply replace the 
  search_query = 'to what you want to scrape'.replace(' ','+') and change the title of the csv file to 
  what is relevant to your topic.

"duplicate_entry_finder.py":

- This program ultilizes "amazon_treadmills_clean.csv" to look for repeated listings
 based on exact matches in name, rating, rating count, and price.
- If exact matches are found, they are removed from the list.
- The new listings are stored in the csv "amazon_treadmills_final.csv".
- *NOTE* As mentioned before, this program can also be used to check duplicates of other products
  that have been scraped, to do so simply change df = pd.read_csv('amazon_treadmills_final.csv') to
  df = pd.read_csv('the_name_of_your_csv').

"treadmill_analyzation.py" :

- This program requires the use of "amazon_treadmills_final.csv" to create the following: 
feature popularity pie chart, price histogram and review count by price range bar chart.
- Certain features like compactness, incline and under desk are looked for throughout the listings and
are created a percentage based on the total number of products.
- The pie chart is saved as "feature_popularity_pie.png".
- Price histogram is created by establishing a price bin of variety of price ranges.
- The total number of listings are counted that fall under a certain price range.
- The histogram is saved as "price_distribution_histogram.png"
- The review count bar chart is created by adding the sum of review counts per price range.
- The bar chart is saved as "review_count_by_price_range.png"


"feature_engagment.py":

-This program requires the use of "amazon_treadmills_final.csv" to create the following: 
feature comparison bar chart.
- Named features are looked for how many listings named them, a total count is given for them.
- Each feature is given an engagement socored based (rating X rating count) of each product that included
the feature.
- The bar chart is saved as "feature_comparison.png"

*NOTE* a copy of "amazon_treadmills_clean.csv" and "amazon_treadmills_final.csv" has been provided
to see the orginal scraped treadmill listings and the final listings.






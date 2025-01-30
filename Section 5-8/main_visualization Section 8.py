# Import necessary libraries
import dash  # Main Dash library for creating web applications
from dash import dcc, html  # Core components and HTML components for the Dash layout
import dash_bootstrap_components as dbc  # Bootstrap components for better styling
import plotly.express as px  # For creating interactive visualizations
import pandas as pd  # For data manipulation and analysis

# Load data from the CSV file
data = pd.read_csv('E:/Python for database/final project/Section 5-8/Finalafter_section7.csv')  
# Convert 'Likes' and 'Retweets' to numeric values to handle non-numeric entries gracefully
data['Likes'] = pd.to_numeric(data['Likes'], errors='coerce')
data['Retweets'] = pd.to_numeric(data['Retweets'], errors='coerce')
# Convert 'Timestamp' column to datetime format for time-based analysis
data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce')

# Create a DataFrame to count the occurrences of each sentiment category
sentiment_counts = data['Sentiment Category'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']  # Rename columns for clarity

# Create a Plotly pie chart to visualize the proportion of sentiment categories
fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', title='Sentiment Distribution')

# Group data by date and sentiment category to create a time-based sentiment distribution
sentiment_time = data.groupby(data['Timestamp'].dt.date)['Sentiment Category'].value_counts().unstack().fillna(0)
# Create a bar chart to show sentiment trends over time
fig_time = px.bar(sentiment_time, x=sentiment_time.index, y=sentiment_time.columns,
                  title='Sentiment Distribution Over Time', labels={'value': 'Count'})

# Create a histogram to show the distribution of likes across tweets
fig_likes = px.histogram(data, x='Likes', nbins=30, title='Likes Distribution')

# Create a scatter plot to visualize the relationship between retweets and likes, categorized by sentiment
fig_retweets_likes = px.scatter(data, x='Retweets', y='Likes', color='Sentiment Category', 
                                title='Retweets vs Likes by Sentiment')

# Create a line chart to show sentiment trends over time
sentiment_time_line = data.groupby(data['Timestamp'].dt.date)['Sentiment Category'].value_counts().unstack().fillna(0)
fig_line = px.line(sentiment_time_line, x=sentiment_time_line.index, y=sentiment_time_line.columns, 
                   title='Sentiment Over Time')

# Initialize the Dash app and apply a Bootstrap theme for improved styling
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard using a container
app.layout = dbc.Container([

    # Title of the dashboard
    html.H1('Sentiment Analysis Dashboard', className='text-center my-4'),

    # Row for displaying sentiment distribution (Pie chart and bar chart over time)
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_pie), width=6),  # Pie chart on the left
        dbc.Col(dcc.Graph(figure=fig_time), width=6),  # Bar chart on the right
    ]),

    # Row for displaying likes distribution and retweets vs likes scatter plot
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_likes), width=6),  # Likes histogram on the left
        dbc.Col(dcc.Graph(figure=fig_retweets_likes), width=6),  # Scatter plot on the right
    ], className='mt-4'),

    # Row for displaying the line chart for sentiment trends over time
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_line), width=12),  # Line chart spanning the full row
    ], className='mt-4'),

    # Dropdown for filtering sentiment categories
    dbc.Row([
        dbc.Col(html.Div([
            html.Label("Select Sentiment Category:"),  # Label for dropdown
            dcc.Dropdown(
                id='sentiment-dropdown',  # Dropdown ID for callback interaction
                options=[  # Options for filtering by sentiment category
                    {'label': 'Positive', 'value': 'Positive'},
                    {'label': 'Negative', 'value': 'Negative'},
                    {'label': 'Neutral', 'value': 'Neutral'},
                    {'label': 'All', 'value': 'All'}  # Option to view all categories
                ],
                value='All',  # Default value
                multi=False  # Single selection only
            )
        ]), width=4),  # Dropdown spans 4 columns in the row
    ], className='mt-4'),

    # Row for displaying a dynamically updated bar chart based on dropdown selection
    dbc.Row([
        dbc.Col(dcc.Graph(id='sentiment-insights-bar-chart'), width=12)  # Placeholder for the bar chart
    ], className='mt-4')

], fluid=True)  # Enable fluid layout for responsive design

# Callback function to update the sentiment insights bar chart based on the dropdown selection
@app.callback(
    dash.dependencies.Output('sentiment-insights-bar-chart', 'figure'),  # Update the bar chart
    [dash.dependencies.Input('sentiment-dropdown', 'value')]  # Input: dropdown value
)
def update_sentiment_insights(selected_sentiment):
    # Filter the data based on the selected sentiment category
    if selected_sentiment == 'All':
        filtered_data = data  # No filtering if 'All' is selected
    else:
        filtered_data = data[data['Sentiment Category'] == selected_sentiment]  # Filter by sentiment
    
    # Count the occurrences of each sentiment in the filtered data
    filtered_sentiment_counts = filtered_data['Sentiment Category'].value_counts().reset_index()
    filtered_sentiment_counts.columns = ['Sentiment', 'Count']  # Rename columns for clarity
    
    # Create a bar chart to visualize the filtered sentiment distribution
    fig_sentiment_insights = px.bar(filtered_sentiment_counts, x='Sentiment', y='Count',
                                    title=f'Sentiment Insights ({selected_sentiment})',
                                    labels={'Sentiment': 'Sentiment Category', 'Count': 'Tweet Count'})
    return fig_sentiment_insights  # Return the updated figure

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)  # Run the app in debug mode for easier troubleshooting

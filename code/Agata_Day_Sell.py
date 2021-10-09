# Dependencies
from datetime import datetime
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 

class DaySell(object):
    all_data = None

    # Constants (Do Not Change)
    _date = "Date"
    _net_purchase = "Net Purchase"
    _gross_sale = "Gross Sale"
    _tax = "Tax"
    _margin = "Margin"
    _line_plot = "line"
    _rel_plot = "rel"
    _box_plot = "box"
    _bar_plot = "bar"
    _year = "Year"
    _month = "Month"
    _day = "Day"
    _resample_daywise = "D"
    _resample_monthwise = "M"
    _resample_yearwise = "A"
    _net_sales = "Net Sales"
    _net_sales_monthly = "Net Sales Monthly"
    _net_average_sales_monthly = "Average Net Sales"
    _net_sales_percentage = "Net Sales Percentage"
    _profit_percentage = "Profit Percentage"
    _data_year = "2018"
    _option_a = "a"
    _option_b = "b"
    _option_c = "c"
    _ordered_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    _day_of_week = 'Day of Week'

    # Variable Constant - Should point to where the file is located in directory
    _file_path = "..\csv\Day_sell_24_12_18.csv"

    def __init__(self):
        """
            Class Initialization
        """
        self.pre_requisite()

    def read_csv_data(self):
        """ 
            Read csv file using pandas read_csv method
        """
        self.all_data = pd.read_csv(self._file_path)

    def display_figure(self, figure_object, title):
        """ 
            Displays the plot in a popup
        """
        plt.title(title)
        plt.show()
        plt.close()

    def rename_columns(self):
        """
            Renames the columns to make data more user friendly
            Date = Date, zn = Net Purchase, sb = Gross Sale, tax = Tax, marza = Margin
        """
        self.columns = [self._date, self._net_purchase, self._gross_sale, self._tax, self._margin]
        self.all_data.columns = self.columns

    def convert_date_type(self):
        """
            Converts the Date columns from object to datetime 
        """
        # Convert Date from Object to Datetime datatype
        self.all_data[self._date] = pd.to_datetime(self.all_data[self._date], dayfirst = True)

        # Set Index
        self.all_data = self.all_data.set_index(self._date)

    def add_more_columns(self):
        """ 
            Add more columns for further filtering the data
        """
        self.all_data[self._year] = self.all_data.index.year
        self.all_data[self._month] = self.all_data.index.month
        self.all_data[self._day_of_week] = self.all_data.index.day_name()

    def clean_data(self):
        """ Dropping last data ,5414124.75,1218719.16,1220682.59,365027.61
            Because its incomplete and will create noise in the data
        """
        self.all_data.drop(len(self.all_data) - 1, inplace = True)

    def reload_data(self):
        """ 
            Reload the data if in case an error occurs
        """
        self.pre_requisite()

    def check_data_consistency(self):
        """ 
            Checks whether all the added columns persist or not
        """
        current_data = self.all_data
        required_columns = [self._year, self._month, self._day_of_week]
        if current_data.columns.any() not in required_columns:
            self.reload_data()

    def pre_requisite(self):
        """ 
            Pre requisite methods to run before performing analysis
        """
        self.read_csv_data()
        self.rename_columns()
        self.clean_data()
        self.convert_date_type()
        self.add_more_columns()

    def get_plot_type(self):
        "Returns the plot type that user wants"
        return input(f'Select plot type ({self._line_plot}, {self._rel_plot}, {self._box_plot}, {self._bar_plot}): ')

    def get_column_name(self):
        """ 
            Returns column name based on the user input
        """
        columns = list(self.all_data.columns)
        # Note: Excludes Year, Month, Day
        columns.remove(self._year)
        columns.remove(self._month)
        columns.remove(self._day_of_week)
        index = 1
        for col in columns:
            print(f'{index}. {col}')
            index += 1
        
        col_number = int(input('Please select column number: '))
        while col_number not in [1, 2, 3, 4]:
            col_number = int(input('Please select column number: '))
        return columns[ col_number - 1]

    def get_from_to_date(self):
        """ 
            Returns range in the form of tuple
            (from_date, to_date)
        """
        from_date = input('From Period (yyyy-mm-dd): ')
        to_date = input('To Period (yyyy-mm-dd): ')

        while datetime.strptime(from_date, '%Y-%m-%d') > datetime.strptime(to_date, '%Y-%m-%d'):
            print('"From Date" cannot be greater than "To Date"')
            from_date = input('From Period (yyyy-mm-dd): ')
            to_date = input('To Period (yyyy-mm-dd): ')

        return (from_date, to_date)

    def summarize_whole_data(self, type_of_plot):
        """
            Displays Lineplot, Relplot, Barplot, Boxplot
            :type_of_plot: 'line', 'rel', 'bar', 'box'
        """
        # Check Consistency
        self.check_data_consistency()

        col_name = self.get_column_name()

        # Set Title
        title = f"Total {col_name} For The Year 2018"

        # Plot
        if type_of_plot in [self._line_plot, self._rel_plot]:
            self.plot_data(type_of_plot, self._date, col_name, self.all_data, title)
        else:
            self.plot_data(type_of_plot, self._month, col_name, self.all_data, title)

    def summarize_whole_data_sum(self, type_of_plot):
        """ 
            Display Sum of the entire column and,
            displays data through: Lineplot, Relplot, Barplot, Boxplot
            Data displayed will be: Monthwise 
        """
        # Check Consistency
        self.check_data_consistency()

        # Get column name:
        col_name = self.get_column_name()

        # Filter Data
        monthly_data = self.all_data.loc[self._data_year].resample(self._resample_monthwise).sum()

        # Set Title
        title = f"Total {col_name} (SUM) For The Year 2018"

        # Plot
        self.plot_data(type_of_plot, self._month, col_name, monthly_data, title)

    def summarize_whole_data_average(self, type_of_plot):
        """ 
            Display Average of the entire column and,
            displays data through: Lineplot, Relplot, Barplot, Boxplot
            Data displayed will be: Monthwise 
        """
        # Check Consistency
        self.check_data_consistency()

        # Get column name:
        col_name = self.get_column_name()

        # Filter Data
        monthly_data = self.all_data.loc[self._data_year].resample(self._resample_monthwise).mean()

        # Set Title
        title = f"Average {col_name} For The Year 2018"

        # Plot
        self.plot_data(type_of_plot, self._month, col_name, monthly_data, title)
    
    def get_net_sales(self, type_of_plot):
        """ 
            Net Sales = Gross Sale - Tax
            Displays data through: Lineplot, Relplot, Barplot, Boxplot
            Data displayed will be: Monthwise 
        """
        # Check Consistency
        self.check_data_consistency()

        # Calculate Net Sales
        self.all_data[self._net_sales] = self.all_data[self._gross_sale] - self.all_data[self._tax]

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_sales, self.all_data[self._data_year], "Net Sales For The Year 2018")

    def get_net_sales_monthly(self, type_of_plot):
        """ 
            Net Sales = Gross Sale - Tax
            Sums up the Net Sales for a particular month
            Displays data through: Lineplot, Relplot, Barplot, Boxplot
            Data displayed will be: Monthwise 
        """
        # Check Consistency
        self.check_data_consistency()

        # Calculate Net Sales
        self.all_data[self._net_sales_monthly] = self.all_data[self._gross_sale] - self.all_data[self._tax]

        # Monthly Data (SUM)
        monthly_data = self.all_data.loc[self._data_year].resample(self._resample_monthwise).sum()

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_sales_monthly, monthly_data, "Monthly Net Sales For The Year 2018")

    def get_average_net_sales_monthly(self, type_of_plot):
        """ 
            Net Sales = Gross Sale - Tax
            Averages the Net Sales for a particular month
            Displays data through: Lineplot, Relplot, Barplot, Boxplot
            Data displayed will be: Monthwise 
        """
        # Check Consistency
        self.check_data_consistency()

        # Calculate Net Sales
        self.all_data[self._net_average_sales_monthly] = self.all_data[self._gross_sale] - self.all_data[self._tax]

        # Monthly Data (SUM)
        monthly_data = self.all_data.loc[self._data_year].resample(self._resample_monthwise).mean()

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_average_sales_monthly, monthly_data, "Monthly Average Net Sales For The Year 2018")

    def get_net_sales_percentage(self, type_of_plot):
        """ 
            Display Net Sales By Percentage Month Wise
        """
        # Check Consistency
        self.check_data_consistency()

        # Calculate Net Sales Percentage
        self.all_data[self._net_sales_percentage] = ((self.all_data[self._gross_sale] - self.all_data[self._tax])/self.all_data[self._gross_sale]) * 100

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_sales_percentage, self.all_data, "Net Sales In Percentage For The Year 2018")

    def get_profit_percentage(self, type_of_plot):
        """ 
            Calculates and displays monthly profit percentage
            Profit Percentage = (Margin / Purchase) * 100
        """
        # Check Consistency
        self.check_data_consistency()

        # Calculate Profit Percentage
        self.all_data[self._profit_percentage] = (self.all_data[self._margin] / self.all_data[self._net_purchase]) * 100

        # Plot
        self.plot_data(type_of_plot, self._month, self._profit_percentage, self.all_data, "Profit Percentage For The Year 2018")

    def display_data_user_choice(self):
        """ 
            Prompts the user to enter Year, Month and Date
            And then segregates data as per user choice
        """
        from_date, to_date = self.get_from_to_date()

        filtered_data = pd.DataFrame(self.all_data.loc[from_date : to_date])

        filtered_data = filtered_data.reset_index()

        filtered_data[self._date] = filtered_data[self._date].dt.date

        plot_type = self.get_plot_type()

        col_name = self.get_column_name()

        # Set Title
        title = f"{col_name} Data From {from_date} to {to_date}"

        self.plot_data(plot_type, self._date, col_name, filtered_data, title)

    def get_total_sales_daywise(self, type_of_plot):
        """
            Display Total Sales Day Wise
        """
        # Add Total Sales
        best_selling_day = self.all_data.groupby(self._day_of_week)[self._gross_sale].sum().reindex(self._ordered_day)

        # Reset Index
        best_selling_day = best_selling_day.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._gross_sale, best_selling_day, "Best Selling Day For The Year 2018")

    def get_average_sales_daywise(self, type_of_plot):
        """
            Display Average Total Sales Day Wise
        """
        # Calculate Average Total Sales Day Wise
        best_selling_day = self.all_data.groupby(self._day_of_week)[self._gross_sale].mean().reindex(self._ordered_day)

        # Reset Index
        best_selling_day = best_selling_day.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._gross_sale, best_selling_day, "Best Selling Day (Average) For The Year 2018")

    def get_profit_daywise(self, type_of_plot):
        """
            Display Profit From Sales Day Wise
        """
        # Calculate Profit Day Wise
        profit = self.all_data.groupby(self._day_of_week)[self._margin].sum().reindex(self._ordered_day)

        # Reset Index
        profit = profit.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._margin, profit, "Profit Earned Day Wise For The Year 2018")

    def get_profit_percentage_daywise(self, type_of_plot):
        """
            Display Profit Percentage Day Wise
        """
        # Calculate Profit Percentage
        self.all_data[self._profit_percentage] = (self.all_data[self._margin] / self.all_data[self._net_purchase]) * 100

        # Add Profit Percentage Day Wise
        profit_percentage = self.all_data.groupby(self._day_of_week)[self._profit_percentage].sum().reindex(self._ordered_day)

        # Reset Index
        profit_percentage = profit_percentage.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._profit_percentage, profit_percentage, "Percentage Profit Earned Day Wise For The Year 2018")

    def plot_data(self, type_of_plot, xvalue, yvalue, data, title):
        """ 
            :type_of_plot: Expected values (line, rel, box, bar) datatype = string
            :xvalue: Column for X-Axis datatype = string
            :yvalue: Column for Y-Axis datatype = string
            :data: Data
        """
        # Plot
        if type_of_plot == self._line_plot:
            figure = sns.lineplot(x=xvalue, y=yvalue, data=data)
        elif type_of_plot == self._rel_plot:
            figure = sns.relplot(x=xvalue, y=yvalue, data=data)
        elif type_of_plot == self._box_plot:
            figure = sns.boxplot(x=xvalue, y=yvalue, data=data)
        else:
            figure = sns.barplot(x=xvalue, y=yvalue, data=data)
        self.display_figure(figure, title)

    def predict_future_tax(self):
        """ 
            Predicts the future tax based on estimates of net purchase and gross sale
            With the predicted future tax, evaluates the margin that will be received
        """
        # Reload the csv file to clear unnecessary columns
        self.read_csv_data()

        # Rename columns
        self.rename_columns()

        # Creates a dataset exclusing Date Margin and Tax, because that will be predicted by model
        train = self.all_data.drop([self._date, self._margin, self._tax], axis=1)

        # Creates a test dataset to test the trained model
        test = self.all_data[self._tax]

        # Creates different training and testing dataset
        # test_size = 0.3 signifies, 30% data will be used for testing and 70% data will be used for training
        x_train, x_test, y_train, y_test = train_test_split(train, test, test_size=0.3, random_state=2)

        # Create LinearRegression object
        simple_regr = LinearRegression()

        # Train the model
        simple_regr.fit(x_train, y_train)

        # Receive input from the user
        net_purchase_assume = float(input('Enter Net Purchase: '))
        gross_sale_assume = float(input('Enter Gross Sale: '))

        # Convert the data to dataframe
        predict_data = pd.DataFrame(np.array([[net_purchase_assume, gross_sale_assume]]), columns=['Net Purchase', 'Gross Sale'])

        # Predict the input
        predicted_tax = simple_regr.predict(predict_data)

        # Get the accuracy of the trained model
        accuracy = simple_regr.score(x_test, y_test) * 100

        # Display the predicted tax with accuracy
        print(f'The predicted tax is {predicted_tax[0]:.2f} with {accuracy:.2f}% accuracy')

        # Calculate margin
        evaluated_margin = gross_sale_assume - (net_purchase_assume + predicted_tax[0])

        # Display margin
        print(f"Evaluated Profit = {evaluated_margin:.2f}")

    def predict_future_purchase_sales(self):
        """ 
            Predicts the future purchase and gross sale based on estimates of tax and margin
            With the predicted future tax, evaluates the margin that will be received
        """
        # Reload the csv file to clear unnecessary columns
        self.read_csv_data()

        # Rename columns
        self.rename_columns()

        # Creates a dataset exclusing Date Margin and Tax, because that will be predicted by model
        train = self.all_data.drop([self._date, self._net_purchase, self._gross_sale], axis=1)

        # Creates a test dataset to test the trained model
        test = self.all_data[[self._net_purchase, self._gross_sale]]

        # Creates different training and testing dataset
        # test_size = 0.3 signifies, 30% data will be used for testing and 70% data will be used for training
        x_train, x_test, y_train, y_test = train_test_split(train, test, test_size=0.3, random_state=2)

        # Create LinearRegression object
        simple_regr = LinearRegression()

        # Train the model
        simple_regr.fit(x_train, y_train)

        # Receive input from the user
        tax_assume = float(input('Enter Tax: '))
        margin_assume = float(input('Enter Margin: '))

        # Convert the data to dataframe
        predict_data = pd.DataFrame(np.array([[tax_assume, margin_assume]]), columns=[self._tax, self._margin])

        # Predict the input
        predicted_purchase_sale = simple_regr.predict(predict_data)

        # Get the accuracy of the trained model
        accuracy = simple_regr.score(x_test, y_test) * 100

        # Display the predicted tax with accuracy
        print(f'The predicted net purchase is {predicted_purchase_sale[0][0]:.2f} and predicted gross sale is {predicted_purchase_sale[0][1]:.2f} with {accuracy:.2f}% accuracy')

def get_plot(day_sell_obj):
    plot = day_sell_obj.get_plot_type()
    while plot not in [day_sell_obj._line_plot, day_sell_obj._rel_plot, day_sell_obj._box_plot, day_sell_obj._bar_plot]:
        plot = day_sell_obj.get_plot_type()
    return plot

def main():
    day_sell_obj = DaySell()
    run = True
    while run:
        print('*' * 30)
        print('Welcome to the Agata Retail Day Sell Data FY 2018')
        print('-' * 30)
        print('1. Display Entire Sales Data')
        print('2. Display Total (SUM) Sales')
        print('3. Display Average Sales')
        print('4. Display Net Sales')
        print('5. Display Net Sales Monthly')
        print('6. Display Average Net Sales')
        print('7. Display Net Sales Percentage')
        print('8. Display Entire Data as per User choice')
        print('9. Display Profit Percentage')
        print('10. Display Total Sale Day wise')
        print('11. Display Average Total Sale Day wise')
        print('12. Display Profit Day wise')
        print('13. Display Profit Percentage Day Wise')
        print('14. Predict Future Tax and Profit')
        print('15. Predict Future Net Purchase and Gross Sale')
        print('16. Quit')
        choice = input('Enter choice: ')
        print('*' * 30)
        if choice == '1':
            day_sell_obj.summarize_whole_data(get_plot(day_sell_obj))
        elif choice == '2':
            day_sell_obj.summarize_whole_data_sum(get_plot(day_sell_obj))
        elif choice == '3':
            day_sell_obj.summarize_whole_data_average(get_plot(day_sell_obj))
        elif choice == '4':
            day_sell_obj.get_net_sales(get_plot(day_sell_obj))
        elif choice == '5':
            day_sell_obj.get_net_sales_monthly(get_plot(day_sell_obj))
        elif choice == '6':
            day_sell_obj.get_average_net_sales_monthly(get_plot(day_sell_obj))
        elif choice == '7':
            day_sell_obj.get_net_sales_percentage(get_plot(day_sell_obj))
        elif choice == '8':
            day_sell_obj.display_data_user_choice()
        elif choice == '9':
            day_sell_obj.get_profit_percentage(get_plot(day_sell_obj))
        elif choice == '10':
            day_sell_obj.get_total_sales_daywise(get_plot(day_sell_obj))
        elif choice == '11':
            day_sell_obj.get_average_sales_daywise(get_plot(day_sell_obj))
        elif choice == '12':
            day_sell_obj.get_profit_daywise(get_plot(day_sell_obj))
        elif choice == '13':
            day_sell_obj.get_profit_percentage_daywise(get_plot(day_sell_obj))
        elif choice == '14':
            day_sell_obj.predict_future_tax()
        elif choice == '15':
            day_sell_obj.predict_future_purchase_sales()
        elif choice == '16':
            run = False
        else:
            print('Invalid choice specified')

if __name__ == '__main__':
    main()
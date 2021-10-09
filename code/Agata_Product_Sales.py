# Dependencies
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime as dt

class Product_Sales_Details(object):

    # Constants
    _file_name = '..\csv\SELL_1.csv'
    _encoding = 'ISO-8859-1'
    _resample_month = 'M'
    _resample_day = 'D'
    _resample_year = 'A'

    # Constants i.e. Name of Rows To Drop
    _pmarza = 'pmarza'
    _pudzmarza = 'pudzmarza'
    _pce_sb = 'pce_sb'
    _pwa_sb = 'pwa_sb'
    _pudz_sb = 'pudzsb'
    _pmarzajedn = 'pmarzajedn'
    _pkwmarza = 'pkwmarza'
    
    # Constants converted to human readable format
    _date = 'Date'
    _product_id = 'ProductID'
    _product_group = 'Product Group'
    _product_name = 'Product Name'
    _product_quantity = 'Product Quantity'
    _net_purchase_price = 'Net Purchase Price'
    _net_purchase_value = 'Net Purchase Value'
    _net_sale_price = 'Net Sale Price'
    _net_sale_value = 'Net Sale Value'
    _net_profit_value = 'Net Profit Value'
    _net_profit_percentage = 'Net Profit Percentage'
    _day = 'Day'
    _month = 'Month'
    _day_of_week = 'Day Of Week'

    # Menu Items
    _incorrect_choice = 'Invalid choice entered. Please select appropriate choice' 
    _get_choice = 'Enter choice: '
    _get_product_group = 'Select Product Group: '
    _view_data = 'How do you wish to view data?'

    # Plot types
    _line_plot = 'line'
    _rel_plot = 'rel'
    _box_plot = 'box'
    _bar_plot = 'bar'

    # Miscelleneuos
    _best_product = 'Best'
    _worst_product = 'Worst'
    _ordered_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def read_data(self):
        """
            Read csv data
        """
        self.file_data = pd.read_csv(self._file_name, encoding = self._encoding)

    def drop_columns(self):
        """ 
            Drops unnecessary columns from the data
        """
        self.file_data = self.file_data.drop([self._pmarza, self._pudzmarza, self._pce_sb, self._pwa_sb, self._pudz_sb, self._pmarzajedn, self._pkwmarza], axis = 1)

    def rename_columns(self):
        """
            Renames the columns to human readable format
        """
        columns = [self._date, self._product_id, self._product_group, self._product_name, self._product_quantity, self._net_purchase_price, self._net_purchase_value, self._net_sale_price, self._net_sale_value]
        self.file_data.columns = columns

    def convert_date_to_datetime(self):
        """
            Convert date to datetime object
        """
        # Convert Date from Object to Datetime datatype
        self.file_data[self._date] = pd.to_datetime(self.file_data[self._date], dayfirst=True, format="%d.%m.%Y")

        # Set Index
        self.file_data = self.file_data.set_index(self._date)

    def add_more_columns(self):
        """ 
            Add more columns - Month, Day
        """
        self.file_data[self._month] = self.file_data.index.month
        self.file_data[self._day_of_week] = self.file_data.index.day_name()

    def get_user_product_group_choice(self, data):
        """ 
            Returns product group selected by user
        """
        index = 1
        unique_product = data[self._product_group].unique()
        print('Product Categories \n')
        user_choice = ''
        run = True
        while run:

            for each_product in unique_product:
                print(f'{index}. {each_product[0]}')
                index += 1
                print('-' * 30)
        
            user_choice = input(self._get_product_group)

            if int(user_choice) in range(1, index):
                break
            else:
                index = 1
                print(self._incorrect_choice)
                continue

        return unique_product[int(user_choice) - 1][0]

    def get_resample_option(self):
        """
            Get sampling method    
        """
        while True:
            print('-' * 30)
            print(f'{self._view_data}')
            print(f'1. {self._day}')
            print(f'2. {self._month}')
            user_choice = input(self._get_choice)
            print('-' * 30)
            if user_choice == '1':
                return self._resample_day
            elif user_choice == '2':
                return self._resample_month
            else:
                print(self._incorrect_choice)

    def get_best_worst(self):
        """
            Returns a string value specifying 'Best' or 'Least'
        """
        validity = True
        user_choose = ''
        while validity:
            print(f'1. {self._best_product}')
            print(f'2. {self._worst_product}')
            user_choice = input(self._get_choice)
            print('-' * 30)

            if user_choice == '1':
                user_choose = self._best_product
                validity = False
            elif user_choice == '2':
                user_choose = self._worst_product
                validity = False
            else:
                print(self._incorrect_choice)

        return user_choose

    # Findings
    def product_group_sales(self, type_of_plot):
        """
            Resamples data daywise, monthwise, yearwise
        """
        # Group By Data
        grouped_data = self.file_data.groupby(self._product_group)

        # Get the resample option
        resample_option = self.get_resample_option()

        # Resample data and sum
        resampled_data = grouped_data[self._product_quantity].resample(resample_option).sum()

        # Reset the index and set index to product group for sorting
        resampled_data = resampled_data.reset_index()
        resampled_data = resampled_data.set_index(self._product_group)

        # Display user list of products
        product_choice = self.get_user_product_group_choice(grouped_data)

        # Sort the data Date wise
        sorted_data = resampled_data

        # Extract data product wise
        product_data = pd.DataFrame(sorted_data.loc[product_choice])

        # Reset index to date to avoid duplicate value error on axis
        product_data = product_data.reset_index()
        if resample_option == self._resample_day:
            product_data[self._date] = product_data[self._date].dt.date
        else:
            product_data[self._date] = product_data[self._date].dt.month

        # Set title
        title = f"Sales Of {product_choice} For The Year 2018"

        # Plot
        self.plot_data(type_of_plot, self._date, self._product_quantity, product_data, title)

    def best_product_group(self):
        """
            Displays best performing product
            Type of plot : Bar plot
        """
        # Group by Product
        product_group = self.file_data.groupby(self._product_group)

        # Calculate the sum of net sales for each product group
        total_sales_product_group = product_group[self._net_sale_value].sum()

        # Reset the index to make product group a part of dataframe
        total_sales_product_group = total_sales_product_group.reset_index()

        # Sort the sales values in ascending order 
        total_sales_product_group = total_sales_product_group.sort_values(by=[self._net_sale_value])

        # Prompt user to get the number of products to be displayed
        products_required = int(input('Number of best products to be displayed: '))

        # Plot
        self.plot_data(self._bar_plot, self._net_sale_value, self._product_group, total_sales_product_group.tail(products_required), "Best Performing Category Of Products For The Year 2018")

    def least_product_group(self):
        """
            Displays least performing product
            Default Type of plot : Bar plot
        """
        # Group by Product
        product_group = self.file_data.groupby(self._product_group)

        # Calculate the sum of net sales for each product group
        total_sales_product_group = product_group[self._net_sale_value].sum()

        # Reset the index to make product group a part of dataframe
        total_sales_product_group = total_sales_product_group.reset_index()

        # Sort the sales values in ascending order 
        total_sales_product_group = total_sales_product_group.sort_values(by=[self._net_sale_value])

        # Prompt user to get the number of products to be displayed
        products_required = int(input('Number of least products to be displayed: '))

        # Plot
        self.plot_data(self._bar_plot, self._net_sale_value, self._product_group, total_sales_product_group.head(products_required), "Least Performing Category Of Products For The Year 2018")

    def get_monthly_net_profit(self, type_of_plot):
        """
            Displays monthly net profit
        """
        # Calculate Net Profit Value
        self.file_data[self._net_profit_value] = self.file_data[self._net_sale_value] - self.file_data[self._net_purchase_value]
        monthly_profit_data = self.file_data[self._net_profit_value].resample(self._resample_month).sum()
        
        # Reset Index
        profit_data = monthly_profit_data.reset_index()

        # Get Month from Date for plotting
        profit_data[self._month] = profit_data[self._date].dt.month

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_profit_value, profit_data, "Monthly Sales Profit For The Year 2018")

    def get_monthly_profit_percentage(self, type_of_plot):
        """
            Displays profit percentage monthly
        """
        # Calculate Profit Percentage
        self.file_data[self._net_profit_percentage] = ((self.file_data[self._net_sale_value] - self.file_data[self._net_purchase_value]) / self.file_data[self._net_purchase_value]) * 100
        monthly_profit_percentage = self.file_data[self._net_profit_percentage].resample(self._resample_month).sum()

        # Reset Index
        percent_profit = monthly_profit_percentage.reset_index()

        # Get Month from Date for plotting
        percent_profit[self._month] = percent_profit[self._date].dt.month

        # Plot
        self.plot_data(type_of_plot, self._month, self._net_profit_percentage, percent_profit, "Monthly Profit Percentage Of Sales For The Year 2018")

    def get_best_product(self, best_or_worst):
        """
            Displays best performing product based on product group
            Default Type of plot : Bar plot
        """
        # Group by Product
        product_group = self.file_data.groupby(self._product_group)

        # Display user list of product groups
        product_group_choice = self.get_user_product_group_choice(product_group)

        # Get List of products according to product group
        products = product_group.get_group(product_group_choice)

        # Convert to dataframe to perform more operations
        products = pd.DataFrame(products).groupby(self._product_name)

        # Sum of sales value
        total_sales = products[self._net_sale_value].sum()

        # Reset index
        total_sales = total_sales.reset_index()

        # Sort by Net Sale Value
        total_sales = total_sales.sort_values(by=[self._net_sale_value])

        # Get user choice number to display the number of products
        products_required = int(input(f'Number of {best_or_worst} products to be displayed: '))

        # Set Title
        title = f"{best_or_worst} Performing Products For The Year 2018 In The Category {product_group_choice}"

        # Plot
        if best_or_worst == self._best_product:
            self.plot_data(self._bar_plot, self._net_sale_value, self._product_name, total_sales.tail(products_required), title)
        else:
            self.plot_data(self._bar_plot, self._net_sale_value, self._product_name, total_sales.head(products_required), title)

    def display_best_selling_day(self, type_of_plot):
        """
            Displays the best selling based on net sale value
        """
        # Add all the total sales day wise
        best_selling_day = self.file_data.groupby(self._day_of_week)[self._net_sale_value].sum().reindex(self._ordered_day)

        # Reset Index
        best_selling_day = best_selling_day.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._net_sale_value, best_selling_day, "Total Sale Day Wise For The Year 2018")

    def average_best_selling_day(self, type_of_plot):
        """
            Display the best selling day based on average of net sale value
        """
        # Calculte average day wise
        best_selling_day = self.file_data.groupby(self._day_of_week)[self._net_sale_value].mean().reindex(self._ordered_day)

        # Reset Index
        best_selling_day = best_selling_day.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._net_sale_value, best_selling_day, "Average Total Sale Day Wise For The Year 2018")

    def get_profit_day_wise(self, type_of_plot):
        """
            Displays total profit earned day wise
        """
        # Calculate Profit
        self.file_data[self._net_profit_value] = self.file_data[self._net_sale_value] - self.file_data[self._net_purchase_value]

        # Add the profit day wise
        profit_data = self.file_data.groupby(self._day_of_week)[self._net_profit_value].sum().reindex(self._ordered_day)

        # Reset Index
        profit_data = profit_data.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._net_profit_value, profit_data, "Net Profit Day Wise For The Year 2018")

    def get_profit_percentage_daywise(self, type_of_plot):
        """
            Displays total profit percentage earned day wise
        """

        # Calculate Profit Percentage
        self.file_data[self._net_profit_percentage] = ((self.file_data[self._net_sale_value] - self.file_data[self._net_purchase_value]) / self.file_data[self._net_purchase_value]) * 100

        # Add the profit day wise
        profit_data = self.file_data.groupby(self._day_of_week)[self._net_profit_percentage].sum().reindex(self._ordered_day)

        # Reset Index
        profit_data = profit_data.reset_index()

        # Plot
        self.plot_data(type_of_plot, self._day_of_week, self._net_profit_percentage, profit_data, "Net Profit Percentage Day Wise For The Year 2018") 
        
    def get_plot_type(self):
        "Returns the plot type that user wants"
        return input(f'Select plot type ({self._line_plot}, {self._rel_plot}, {self._box_plot}, {self._bar_plot}): ')

    def display_figure(self, figure_object, title):
        """ 
            Displays the plot in a popup
        """
        plt.title(title)
        plt.show()
        plt.close()

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

    def __init__(self):
        """ Class Initialisation """
        self.file_data = None
        self.read_data()
        self.drop_columns()
        self.rename_columns()
        self.convert_date_to_datetime()
        self.add_more_columns()

def get_plot(product_sales_obj):
    plot = product_sales_obj.get_plot_type()
    while plot not in [product_sales_obj._line_plot, product_sales_obj._rel_plot, product_sales_obj._box_plot, product_sales_obj._bar_plot]:
        plot = product_sales_obj.get_plot_type()
    return plot

def main():
    product_sales_obj = Product_Sales_Details()
    run = True
    while run:
        print('-' * 30)
        print('1. Display Product Sales')
        print('2. Display Best Performing Product Category')
        print('3. Display Least Performing Product Group')
        print('4. Display Monthly Net Profit')
        print('5. Display Monthly Profit Percentage')
        print('6. Display Best / Worst Performing Product')
        print('7. Display Best Selling Day in Week')
        print('8. Display Average Best Selling Day In Week')
        print('9. Display Profit In Value Daywise')
        print('10. Display Profit In Percentage Daywise')
        print('11. Quit')
        user_choice = input(product_sales_obj._get_choice)
        print('-' * 30)
        if user_choice == '1':
            plot = get_plot(product_sales_obj)
            product_sales_obj.product_group_sales(plot)
        elif user_choice == '2':
            product_sales_obj.best_product_group()
        elif user_choice == '3':
            product_sales_obj.least_product_group()
        elif user_choice == '4':
            plot = get_plot(product_sales_obj)
            product_sales_obj.get_monthly_net_profit(plot)
        elif user_choice == '5':
            plot = get_plot(product_sales_obj)
            product_sales_obj.get_monthly_profit_percentage(plot)
        elif user_choice == '6':
            user_choose = product_sales_obj.get_best_worst()
            product_sales_obj.get_best_product(user_choose)
        elif user_choice == '7':
            plot = get_plot(product_sales_obj)
            product_sales_obj.display_best_selling_day(plot)
        elif user_choice == '8':
            plot = get_plot(product_sales_obj)
            product_sales_obj.average_best_selling_day(plot)
        elif user_choice == "9":
            plot = get_plot(product_sales_obj)
            product_sales_obj.get_profit_day_wise(plot)
        elif user_choice == "10":
            plot = get_plot(product_sales_obj)
            product_sales_obj.get_profit_percentage_daywise(plot)
        elif user_choice == '11':
            run = False
        else:
            print(product_sales_obj._incorrect_choice)

if __name__ == '__main__':
    main()

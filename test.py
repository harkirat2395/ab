import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu

st.title("Welcome to My Project")
st.sidebar.header("Sidebar")
crime_options = ["Please Choose a Crime", "Rape", "Frauds", "Kidnapping","Custodial Death",'Causes of Murders','Murders']
crime_type = st.sidebar.selectbox("Types of Crime", options=crime_options)
dataframes = {
    "Rape": pd.read_csv("20_Victims_of_rape.csv"),
    "Frauds": pd.read_csv('10_Property_stolen_and_recovered.csv'),
    "Kidnapping": pd.read_csv('39_Specific_purpose_of_kidnapping_and_abduction.csv'),
    "Custodial Death":pd.read_csv('40_05_Custodial_death_others.csv'),
    "Murders":pd.read_csv('32_Murder_victim_age_sex.csv'),
    'Causes of Murders':pd.read_csv("19_Motive_or_cause_of_murder_and_culpable_homicide_not_amounting_to_murder.csv")
                                                                }

if crime_type != "Please Choose a Crime":
    st.sidebar.header("Menu")

    if crime_type == "Rape":
        df = dataframes["Rape"]
        with st.sidebar:
            selected_option = option_menu(
                "India Crime Data",
                ["See Dataset", "Cases Reported Yearly", "Cases Reported in States",
                 "Victim's Between 10-14", "Rape Cases of Different Age Groups (Bar Chart)",
                 "Incest and Other Rapes", "Rape Cases of Different Age Groups (Pie Chart)",
                 "Multiple States"],
                icons=["question-circle", "table", "calendar", "bar-chart", "person-bounding-box", "bar-chart", "bar-chart", "pie-chart", "map"],
                menu_icon="cast",
                default_index=0
            )

            st.subheader("Details of Crimes")

        if selected_option == "See Dataset":
            st.write(df)

        elif selected_option == "Cases Reported Yearly":
            yearly_cases = df.groupby("Year")["Rape_Cases_Reported"].sum().reset_index()
            fig = px.line(yearly_cases, x='Year', y='Rape_Cases_Reported', markers=True,
                          title='Rape Cases Reported Yearly (2001-2010)',
                          labels={'Year': 'Year', 'Rape_Cases_Reported': 'Rape Cases Reported'})
            fig.update_traces(mode='lines+markers')
            fig.update_layout(xaxis_title='Year', yaxis_title='Rape Cases Reported', xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_option == "Cases Reported in States":
            fig = px.bar(df, x="Area_Name", y="Rape_Cases_Reported", color="Rape_Cases_Reported",
                         color_continuous_scale='viridis',
                         title='Rape Cases Reported in States',
                         labels={'Area_Name': 'Area Name', 'Rape_Cases_Reported': 'Rape Cases Reported'})
            fig.update_layout(xaxis_title='Area Name', yaxis_title='Rape Cases Reported', xaxis_tickangle=-90)
            st.plotly_chart(fig)

        elif selected_option == "Victim's Between 10-14":
            fig = px.bar(df, x="Area_Name", y="Victims_Between_10-14_Yrs", color="Victims_Between_10-14_Yrs",
                         color_continuous_scale='viridis',
                         title="Victims Between 10-14 Years Old in Different Areas",
                         labels={'Area_Name': 'Area Name', 'Victims_Between_10-14_Yrs': 'Victims Between 10-14 Yrs'})
            fig.update_layout(xaxis_title='Area Name', yaxis_title='Victims Between 10-14 Yrs', xaxis_tickangle=-90)
            st.plotly_chart(fig)

        elif selected_option == "Rape Cases of Different Age Groups (Bar Chart)":
            age_group_data = df[['Victims_Upto_10_Yrs', 'Victims_Between_10-14_Yrs',
                                'Victims_Between_14-18_Yrs', 'Victims_Between_18-30_Yrs',
                                'Victims_Between_30-50_Yrs', 'Victims_Above_50_Yrs']].sum().reset_index()
            age_group_data.columns = ['Age_Group', 'Total_Victims']

            fig = px.bar(age_group_data, x='Age_Group', y='Total_Victims', color='Total_Victims',
                         color_continuous_scale='viridis',
                         title='Distribution of Victims by Age Group (2001-2012)',
                         labels={'Age_Group': 'Age Group', 'Total_Victims': 'Total Victims'})
            fig.update_layout(xaxis_title='Age Group', yaxis_title='Total Victims', xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_option == "Incest and Other Rapes":
            incest_rape_victims = df[df['Subgroup'] == 'Victims of Incest Rape']
            other_rape_victims = df[df['Subgroup'] == 'Victims of Other Rape']

            incest_rape_agg = incest_rape_victims.groupby('Year')['Victims_of_Rape_Total'].sum().reset_index()
            other_rape_agg = other_rape_victims.groupby('Year')['Victims_of_Rape_Total'].sum().reset_index()

            comparison_data = incest_rape_agg.merge(other_rape_agg, on='Year', suffixes=('_Incest', '_Other'))

            fig = px.line(comparison_data, x='Year', y=['Victims_of_Rape_Total_Incest', 'Victims_of_Rape_Total_Other'],
                          labels={'value': 'Total Victims', 'variable': 'Type of Rape'},
                          title='Comparison of Incest and Other Rape Cases (2001-2012)',
                          color_discrete_map={'Victims_of_Rape_Total_Incest': 'red', 'Victims_of_Rape_Total_Other': 'green'})
            fig.update_layout(xaxis_title='Year', yaxis_title='Total Victims', xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_option == "Rape Cases of Different Age Groups (Pie Chart)":
            age_group_data = df[['Victims_Upto_10_Yrs', 'Victims_Between_10-14_Yrs',
                                'Victims_Between_14-18_Yrs', 'Victims_Between_18-30_Yrs',
                                'Victims_Between_30-50_Yrs', 'Victims_Above_50_Yrs']].sum()

            fig = px.pie(values=age_group_data, names=age_group_data.index,
                         title='Pie Chart: Distribution of Victims by Age Group (2001-2012)',
                         labels={'index': 'Age Group', 'value': 'Total Victims'})
            st.plotly_chart(fig)

        elif selected_option == "Multiple States":
            selected_states = st.sidebar.multiselect(
                "Select states",
                options=df['Area_Name'].unique(),
                default=["Delhi", "Punjab", "West Bengal"]
            )

            multi_state_data = df[df['Area_Name'].isin(selected_states) & (df['Subgroup'] == 'Total Rape Victims')]

            fig = px.line(multi_state_data, x='Year', y='Victims_of_Rape_Total', color='Area_Name',
                          title='Year vs Total Rape Victims in Selected States',
                          labels={'Year': 'Year', 'Victims_of_Rape_Total': 'Total Rape Victims'})
            fig.update_layout(xaxis_title='Year', yaxis_title='Total Rape Victims', xaxis_tickangle=-45)
            st.plotly_chart(fig)

    elif crime_type == "Frauds":
        df = dataframes["Frauds"]
        df = df.dropna()  # Drop missing values
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        corr_matrix = numeric_df.corr()
        with st.sidebar:
            selected_option = option_menu(
                "Property Theft and Recovery Data",
                ["See Dataset", "Subgroups and Groups", "Property Stolen and Recovered Over the Years",
                 "Bar Plot for Stolen and Recovered Property by States", "Pie Chart for Total Property Stolen and Recovered",
                 "Scatter Plot for Stolen vs Recovered Property", "Heatmap for Correlation",
                 "Boxplot for Distribution of Stolen and Recovered Property Values"],
                icons=["person-plus-fill", "table", "geo-alt", "line-chart", "bar-chart", "pie-chart", "scatter", "heatmap", "bar-chart"],
                menu_icon="cast",
                default_index=0
            )

        st.subheader("Details of Crimes")

        if selected_option == "See Dataset":
            st.write(df)
            st.write(df.head())
            st.write(df.describe())

        elif selected_option == "Property Stolen and Recovered Over the Years":
            fig = px.line(df, x='Year', y=['Value_of_Property_Stolen', 'Value_of_Property_Recovered'],
                          labels={'value': 'Value (in crores)', 'variable': 'Property Type'},
                          title='Property Stolen and Recovered Over the Years',
                          color_discrete_map={'Value_of_Property_Stolen': 'blue', 'Value_of_Property_Recovered': 'green'})
            fig.update_layout(xaxis_title='Year', yaxis_title='Value (in crores)', xaxis_tickangle=-45)
            st.plotly_chart(fig)

        elif selected_option == "Subgroups and Groups":
         st.title("Property Stolen by Subgroup Over Time")
         subgroups = df['Sub_Group_Name'].unique()
         selected_subgroup = st.sidebar.selectbox(
            "Select Subgroup",
            options=subgroups,
            index=0
         )
         selected_states = st.sidebar.multiselect(
            "Select States",
            options=df['Area_Name'].unique(),
            default=["Delhi", "Punjab", "West Bengal"]
         )
         filtered_data = df[(df['Area_Name'].isin(selected_states)) & (df['Sub_Group_Name'] == selected_subgroup)]
          #st.write(filtered_data)
         fig = px.line(
         filtered_data,
         x='Year',
         y='Value_of_Property_Stolen',
         color='Area_Name',
         markers=True,
         title=f'Property Stolen in Selected States for Subgroup: {selected_subgroup} Over Time',
         labels={'Year': 'Year', 'Value_of_Property_Stolen': 'Value of Property Stolen (Rs. in Crore)', 'Area_Name': 'Area Name'},
         line_shape='linear'
            )
         fig.update_layout(
         xaxis_title='Year',
         yaxis_title='Value of Property Stolen (Rs. in Crore)',
         xaxis_tickangle=-45,
         legend_title='Area Name',
         legend=dict(
            title='Area Name',
            x=1.05,
            y=1,
            traceorder='normal',
            orientation='v'
            )
            )
         st.plotly_chart(fig)
        elif selected_option == "Bar Plot for Stolen and Recovered Property by States":
            fig = px.bar(df, x='Area_Name', y=['Value_of_Property_Stolen', 'Value_of_Property_Recovered'],
                         labels={'value': 'Value (in crores)', 'Area_Name': 'State'},
                         title='Property Stolen and Recovered by States',
                         color_discrete_map={'Value_of_Property_Stolen': 'red', 'Value_of_Property_Recovered': 'green'})
            fig.update_layout(xaxis_title='State', yaxis_title='Value (in crores)', xaxis_tickangle=-90)
            st.plotly_chart(fig)
        elif selected_option == "Pie Chart for Total Property Stolen and Recovered":
            total_stolen = df['Value_of_Property_Stolen'].sum()
            total_recovered = df['Value_of_Property_Recovered'].sum()

            fig = px.pie(values=[total_stolen, total_recovered], names=['Total Stolen', 'Total Recovered'],
                         title='Pie Chart: Total Property Stolen vs Recovered',
                         labels={'names': 'Property Type', 'values': 'Value (in crores)'})
            st.plotly_chart(fig)
        elif selected_option == "Scatter Plot for Stolen vs Recovered Property":
            fig = px.scatter(
             df,
             x='Value_of_Property_Stolen',
             y='Value_of_Property_Recovered',
             color='Area_Name',
             title='Scatter Plot for Stolen vs Recovered Property',
             labels={'Value_of_Property_Stolen': 'Value of Property Stolen (in Crores)', 'Value_of_Property_Recovered': 'Value of Property Recovered (in Crores)'},
             color_discrete_sequence=px.colors.qualitative.Plotly,
             hover_name='Area_Name',
             hover_data={'Value_of_Property_Stolen': True, 'Value_of_Property_Recovered': True},
             size_max=20  
                                                            )
            fig.update_layout(
             xaxis_title='Value of Property Stolen (in Crores)',
             yaxis_title='Value of Property Recovered (in Crores)',
             legend_title='Area Name',
             xaxis=dict(showgrid=True,showline=True,showticklabels=True),
             yaxis=dict(showgrid=True,showline=True,showticklabels=True),
             legend=dict(title='Area Name',x=1.05,y=1,traceorder='normal',orientation='v')
             )
            st.plotly_chart(fig)
        elif selected_option == "Heatmap for Correlation":
            fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='viridis',
                            title='Heatmap of Correlation Matrix',
                            labels={'x': 'Features', 'y': 'Features'})
            st.plotly_chart(fig)
        elif selected_option == "Boxplot for Distribution of Stolen and Recovered Property Values":
            fig = px.box(df.melt(id_vars='Year', value_vars=['Value_of_Property_Stolen', 'Value_of_Property_Recovered']),
                         x='variable', y='value',
                         title='Boxplot for Distribution of Stolen and Recovered Property Values',
                         labels={'variable': 'Property Type', 'value': 'Value (in crores)'})
            st.plotly_chart(fig)
    elif crime_type == "Kidnapping":
     df = dataframes["Kidnapping"]
     df.rename(columns={
        "K_A_Female_10_15_Years": "Female 10-15 Years",
        "K_A_Female_15_18_Years": "Female 15-18 Years",
        "K_A_Female_18_30_Years": "Female 18-30 Years",
        "K_A_Female_30_50_Years": "Female 30-50 Years",
        "K_A_Female_Above_50_Years": "Female Above 50 Years",
        "K_A_Female_Total": "Female Total",
        "K_A_Female_Upto_10_Years": "Female Upto 10 Years",
        "K_A_Grand_Total": "Grand Total",
        "K_A_Male_10_15_Years": "Male 10-15 Years",
        "K_A_Male_15_18_Years": "Male 15-18 Years",
        "K_A_Male_18_30_Years": "Male 18-30 Years",
        "K_A_Male_30_50_Years": "Male 30-50 Years",
        "K_A_Male_Above_50_Years": "Male Above 50 Years",
        "K_A_Male_Total": "Male Total",
        "K_A_Male_Upto_10_Years": "Male Upto 10 Years"
          }, inplace=True)
    
     with st.sidebar:
        selected_option = option_menu(
            "Kidnapping and Abduction Data",
            ["See Dataset", "Kidnapping Cases Reported Yearly", "Kidnapping Cases in States",
             "Specific Purpose of Kidnapping and Abduction", "Trend of Kidnapping Over the Years", "Custom Column Analysis"],
            icons=["question-circle", "table", "calendar", "person-bounding-box", "bar-chart", "pie-chart", "bar-chart"],
            menu_icon="cast",
            default_index=0
          )

     st.subheader("Details of Crimes")

     if selected_option == "See Dataset":
        st.write(df)

     elif selected_option == "Kidnapping Cases Reported Yearly":
        yearly_cases = df.groupby("Year")["K_A_Cases_Reported"].sum().reset_index()
        fig = px.line(
            yearly_cases,
            x='Year',
            y='K_A_Cases_Reported',
            markers=True,
            title='Kidnapping Cases Reported Yearly (2001-2012)',
            labels={'K_A_Cases_Reported': 'Kidnapping Cases Reported'}
         )
        fig.update_traces(line=dict(color='blue'))
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Kidnapping Cases Reported',
            xaxis_tickangle=-45,
            template='plotly_white'
         )
        st.plotly_chart(fig)

     elif selected_option == "Kidnapping Cases in States":
        fig = px.bar(
            df,
            x="Area_Name",
            y="K_A_Cases_Reported",
            title='Kidnapping Cases Reported in States',
            labels={'Area_Name': 'Area Name', 'K_A_Cases_Reported': 'Kidnapping Cases Reported'},
            color='K_A_Cases_Reported',
         )
        fig.update_layout(
            xaxis_title='Area Name',
            yaxis_title='Kidnapping Cases Reported',
            xaxis_tickangle=-90,
        )
        st.plotly_chart(fig)

     elif selected_option == "Specific Purpose of Kidnapping and Abduction":
        purpose_data = df.groupby("Sub_Group_Name")["K_A_Cases_Reported"].sum().reset_index()
        fig = px.bar(
            purpose_data,
            x="Sub_Group_Name",
            y="K_A_Cases_Reported",
            title='Specific Purpose of Kidnapping and Abduction',
            labels={'Sub_Group_Name': 'Purpose', 'K_A_Cases_Reported': 'Cases Reported'},
            color='K_A_Cases_Reported',
            color_continuous_scale='viridis'
        )
        fig.update_layout(
            xaxis_title='Purpose',
            yaxis_title='Cases Reported',
            xaxis_tickangle=-90,
            template='plotly_white'
        )
        st.plotly_chart(fig)

     elif selected_option == "Trend of Kidnapping Over the Years":
         subgroups = df['Sub_Group_Name'].unique()
         selected_subgroup = st.sidebar.selectbox(
            "Select Subgroup",
            options=subgroups,
            index=0
         )
         selected_states = st.sidebar.multiselect(
            "Select States",
            options=df['Area_Name'].unique(),
            default=["Delhi", "Punjab", "West Bengal"]
         )
         filtered_data = df[(df['Area_Name'].isin(selected_states))& (df['Sub_Group_Name'] == selected_subgroup)]
         fig = px.line(
         filtered_data,
         x='Year',
         y='K_A_Cases_Reported',
         color='Area_Name',
         markers=True,
         title=f'Property Stolen in Selected States for Subgroup: {selected_subgroup} Over Time',
         labels={'Year': 'Year', 'K_A_Cases_Reported': 'Cases Reported', 'Area_Name': 'Area Name'},
         line_shape='linear'
            )
         fig.update_layout(
         xaxis_title='Year',
         yaxis_title='Cases Reported',
         xaxis_tickangle=-45,
         legend_title='Area Name',
         legend=dict(
            title='Area Name',
            x=1.05,
            y=1,
            traceorder='normal',
            orientation='v'
            )
            )
         st.plotly_chart(fig)
     elif selected_option == "Custom Column Analysis":
        columns = [
            "Female 10-15 Years", "Female 15-18 Years", "Female 18-30 Years",
            "Female 30-50 Years", "Female Above 50 Years", "Female Total",
            "Female Upto 10 Years", "Grand Total", "Male 10-15 Years",
            "Male 15-18 Years", "Male 18-30 Years", "Male 30-50 Years",
            "Male Above 50 Years", "Male Total", "Male Upto 10 Years"
        ]
        selected_columns = st.sidebar.multiselect(
            "Select Columns",
            options=columns,
            default=["Female 10-15 Years", "Female 15-18 Years"]
        )

        if selected_columns:
            column_data = df[selected_columns].sum().reset_index()
            column_data.columns = ['Column', 'Total']

            fig = px.bar(
                column_data,
                x='Column',
                y='Total',
                title='Total Kidnapping Cases by Selected Columns',
                labels={'Column': 'Columns', 'Total': 'Total Cases'},
                color='Total',
                color_continuous_scale='viridis'
            )
            fig.update_layout(
                xaxis_title='Columns',
                yaxis_title='Total Cases',
                xaxis_tickangle=-45,
                template='plotly_white'
            )
            st.plotly_chart(fig)
    elif crime_type == "Custodial Death":
     df = dataframes["Custodial Death"]
     df.fillna(0, inplace=True)
     df['Total_Deaths'] = df.iloc[:, 4:].sum(axis=1)
    
     with st.sidebar:
        selected_option = option_menu(
            "Custodial Death Data",
            ["See Dataset", "Trend of Custodial Deaths Over the Years", "Custodial Deaths by State",
             "Causes of Custodial Deaths", "Yearly Distribution of Causes of Death", "Top States with the Highest Custodial Deaths"],
            icons=["question-circle", "line-chart", "bar-chart", "pie-chart", "area-chart", "bar-chart"],
            menu_icon="cast",
            default_index=0
                                  )
    
     st.subheader("Details of Custodial Deaths")

     if selected_option == "See Dataset":
        st.write(df)

     elif selected_option == "Trend of Custodial Deaths Over the Years":
        trend_df = df.groupby('Year')['Total_Deaths'].sum().reset_index()
        fig_trend = px.line(trend_df, x='Year', y='Total_Deaths', title='Trend of Custodial Deaths Over the Years')
        st.plotly_chart(fig_trend)

     elif selected_option == "Custodial Deaths by State":
        state_df = df.groupby('Area_Name')['Total_Deaths'].sum().reset_index()
        fig_state = px.bar(state_df, x='Area_Name', y='Total_Deaths', title='Custodial Deaths by State', 
                           labels={'Area_Name': 'State', 'Total_Deaths': 'Total Deaths'},
                           height=600)
        fig_state.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig_state)

     elif selected_option == "Causes of Custodial Deaths":
        cause_df = df.melt(id_vars=['Area_Name', 'Year'], 
                          value_vars=['CD_Accidents', 'CD_By_Mob_AttackRiots', 'CD_By_other_Criminals', 
                                      'CD_By_Suicide', 'CD_IllnessNatural_Death', 'CD_While_Escaping_from_Custody'],
                          var_name='Cause', value_name='Deaths')
        cause_df = cause_df.groupby('Cause')['Deaths'].sum().reset_index()
        fig_cause = px.pie(cause_df, values='Deaths', names='Cause', title='Causes of Custodial Deaths')
        st.plotly_chart(fig_cause)

     elif selected_option == "Yearly Distribution of Causes of Death":
        yearly_cause_df = df.melt(id_vars=['Year'], 
                                 value_vars=['CD_Accidents', 'CD_By_Mob_AttackRiots', 'CD_By_other_Criminals', 
                                             'CD_By_Suicide', 'CD_IllnessNatural_Death', 'CD_While_Escaping_from_Custody'],
                                 var_name='Cause', value_name='Deaths')
        yearly_cause_df = yearly_cause_df.groupby(['Year', 'Cause'])['Deaths'].sum().reset_index()
        fig_yearly_cause = px.area(yearly_cause_df, x='Year', y='Deaths', color='Cause', title='Yearly Distribution of Causes of Death')
        st.plotly_chart(fig_yearly_cause)

     elif selected_option == "Top States with the Highest Custodial Deaths":
        top_states_df = state=df.sort_values(by='Total_Deaths', ascending=False).head(10)
        fig_top_states = px.bar(top_states_df, x='Area_Name', y='Total_Deaths', title='Top States with the Highest Custodial Deaths', 
                              labels={'Area_Name': 'State', 'Total_Deaths': 'Total Deaths'})
        st.plotly_chart(fig_top_states)
    elif crime_type == "Murders":
     df = dataframes["Murders"]
     df.fillna(0, inplace=True)
     with st.sidebar:
        selected_option = option_menu(
            "Murder Data",
            ["See Dataset", "Total Number of Victims by Area for a Specific Year", 
             "Pie Chart: Distribution of Victims by Age Group for a Specific Area and Year", 
             "Trends of Total Victims Over the Years for a Specific Area"],
            icons=["question-circle", "bar-chart", "pie-chart", "line-chart"],
            menu_icon="cast",
            default_index=0
        )

     st.subheader("Details of Murders")

     if selected_option == "See Dataset":
        st.write(df)

     elif selected_option == "Total Number of Victims by Area for a Specific Year":
        # Sidebar input for the year
        year = st.sidebar.slider("Select Year", min_value=df['Year'].min(), max_value=df['Year'].max(), value=df['Year'].min())
        data_year = df[df['Year'] == year]
        
        fig_bar = px.bar(data_year, x='Area_Name', y='Victims_Total', 
                        title=f'Total Number of Victims by Area ({year})',
                        labels={'Victims_Total': 'Total Victims', 'Area_Name': 'Area'},
                        color='Victims_Total', 
                        color_continuous_scale='Viridis')
        fig_bar.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig_bar)

     elif selected_option == "Pie Chart: Distribution of Victims by Age Group for a Specific Area and Year":
        # Sidebar inputs for the area and year
        area = st.sidebar.selectbox("Select Area", options=df['Area_Name'].unique(), index=0)
        year = st.sidebar.slider("Select Year", min_value=df['Year'].min(), max_value=df['Year'].max(), value=df['Year'].min())
        data_area_year = df[(df['Area_Name'] == area) & (df['Year'] == year)]
        
        # Prepare data for the pie chart
        age_groups = ['Victims_Above_50_Yrs', 'Victims_Upto_10_15_Yrs', 'Victims_Upto_10_Yrs',
                      'Victims_Upto_15_18_Yrs', 'Victims_Upto_18_30_Yrs', 'Victims_Upto_30_50_Yrs']
        age_group_labels = ['Above 50 Yrs', '10-15 Yrs', 'Up to 10 Yrs', '15-18 Yrs', '18-30 Yrs', '30-50 Yrs']
        age_group_values = data_area_year[age_groups].sum().values

        fig_pie = px.pie(names=age_group_labels, values=age_group_values,
                        title=f'Distribution of Victims by Age Group ({area}, {year})')
        st.plotly_chart(fig_pie)

     elif selected_option == "Trends of Total Victims Over the Years for a Specific Area":
        # Sidebar input for the area
        area = st.sidebar.selectbox("Select Area", options=df['Area_Name'].unique(), index=0)
        data_area = df[df['Area_Name'] == area]
        
        fig_line = px.line(data_area, x='Year', y='Victims_Total', markers=True,
                          title=f'Trends of Total Victims Over the Years for {area}',
                          labels={'Victims_Total': 'Total Victims', 'Year': 'Year'})
        fig_line.update_traces(line=dict(color='blue'))
        fig_line.update_layout(xaxis_title='Year', yaxis_title='Total Victims', xaxis_tickangle=-45)
        st.plotly_chart(fig_line)
    elif crime_type == 'Causes of Murders':
     df=dataframes["Causes of Murders"]
       
     with st.sidebar:
      selected_option = option_menu(
        "Murder Data",
        ["See Dataset", 
        "Total Number of Victims by Area for a Specific Year",
        "Pie Chart: Distribution of Victims by Age Group for a Specific Area and Year",
        "Trends of Total Victims Over the Years for a Specific Area",
        "Grouped Bar Chart by Murder Cause",
        "Stacked Bar Chart by Murder Cause",
        "Pie Chart of Murder Causes for 2005",
        "Scatter plot of Murder Causes Over Time",
        "Heat Map of Murder Causes",
        "Total Murder Causes Comparison"],
        icons=["table", "bar-chart", "pie-chart", "line-chart", "bar-chart", "bar-chart", "pie-chart", "line-chart", "heatmap", "area-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0
                                                                     )

     st.subheader("Details of Murders")

            # Display the dataset
     if selected_option == "See Dataset":
      df_sorted = df.sort_values(by=['Area_Name', 'Year']).reset_index(drop=True)
      st.subheader("Dataset: Sorted by Area and Year")
      st.write(df_sorted)

        # Total Number of Victims by Area for a Specific Year
     elif selected_option == "Total Number of Victims by Area for a Specific Year":
        # Aggregate data by Area_Name and sum up Murder_Cause_Total across all years
        data_agg = df.groupby('Area_Name')['Murder_Cause_Total'].sum().reset_index()

        # Sidebar to select the option
        selected_option = st.sidebar.selectbox("Choose an option", ["Total Number of Victims by Area for a Specific Year", "Total Number of Victims by Area across All Years"])

        if selected_option == "Total Number of Victims by Area for a Specific Year":
            year = st.sidebar.slider("Select Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=int(df['Year'].min()))
            data_year = df[df['Year'] == year].reset_index(drop=True)
            
            fig_bar = px.bar(data_year, x='Area_Name', y='Murder_Cause_Total', 
                            title=f'Total Number of Victims by Area ({year})',
                            labels={'Murder_Cause_Total': 'Total Victims', 'Area_Name': 'Area'},
                            color='Murder_Cause_Total', color_continuous_scale='Viridis')
            
            fig_bar.update_layout(xaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar)

        elif selected_option == "Total Number of Victims by Area across All Years":
            fig_bar_all_years = px.bar(data_agg, x='Area_Name', y='Murder_Cause_Total',
                                    title='Total Number of Victims by Area (Across All Years)',
                                    labels={'Murder_Cause_Total': 'Total Victims', 'Area_Name': 'Area'},
                                    color='Murder_Cause_Total', color_continuous_scale='Viridis')
            
            fig_bar_all_years.update_layout(xaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar_all_years)
      # Pie Chart: Distribution of Victims by Age Group for a Specific Area and Year
     elif selected_option == "Pie Chart: Distribution of Victims by Age Group for a Specific Area and Year":
      st.title("Distribution of Victims by Age Group")
    
        # Allow user to select area and year
      area = st.sidebar.selectbox("Select Area", options=df['Area_Name'].unique(), index=0)
      year = st.sidebar.slider("Select Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=int(df['Year'].min()))
        
        # Allow user to select causes of murder
      types_of_murder = ['Murder_Cause_By_TerroristExtremist',
                        'Murder_Cause_Casteism', 'Murder_Cause_Class_Conflict', 'Murder_Cause_Communalism',
                        'Murder_Cause_Dowry', 'Murder_Cause_For_Political_reason',
                        'Murder_Cause_Love_AffairsSexual_Relations', 'Murder_Cause_Lunacy',
                        'Murder_Cause_Other_Causes_or_Motives', 'Murder_Cause_Personal_Vendetta_or_Enmity',
                        'Murder_Cause_Property_Dispute', 'Murder_Cause_Witchcraft']
        
      selected_causes = st.sidebar.multiselect(
            "Select Causes of Murder",
            options=types_of_murder,
            default=types_of_murder
        )
        
        # Filter data based on selected area and year
      data_area_year = df[(df['Year'] == year) & (df['Area_Name'] == area)]
        
        # Extract values for selected causes of murder
      age_group_values = data_area_year[selected_causes].values.flatten()
      cause_labels = [cause.split('_')[-1] for cause in selected_causes]  # Extract labels for the causes
        
        # Plot pie chart
      fig_pie = px.pie(names=cause_labels,values=age_group_values,
                       title=f'Distribution of Victims by Age Group ({area}, {year})' )
      st.plotly_chart(fig_pie)

      # Trends of Total Victims Over the Years for a Specific Area
     elif selected_option == "Trends of Total Victims Over the Years for a Specific Area":
         df = df.sort_values(by=['Area_Name']).reset_index(drop=True)
             # Allow user to select multiple areas
         selected_areas = st.sidebar.multiselect("Select Areas", options=df['Area_Name'].unique(), default=[df['Area_Name'].unique()[0]])
        
         # Filter data for selected areas
         data_areas = df[df['Area_Name'].isin(selected_areas)]
        
          # Plot trends for selected areas using Plotly Express
         fig = px.line(data_areas, x='Year', y='Murder_Cause_Total', color='Area_Name',
                    title='Trends of Total Victims Over the Years',
                    labels={'Year': 'Year', 'Murder_Cause_Total': 'Total Victims', 'Area_Name': 'Area'})
        
         fig.update_layout(xaxis_title='Year', yaxis_title='Total Victims', xaxis_tickangle=-45)
         st.plotly_chart(fig)


      # Grouped Bar Chart by Murder Cause
     elif selected_option == "Grouped Bar Chart by Murder Cause":
        selected_state = st.sidebar.selectbox("Select State", options=df['Area_Name'].unique(), index=0)
        
        # Convert column names to Python list for options and default
        options = list(df.columns[2:16])  # Assuming 2:16 are the columns of interest for causes
        default = list(df.columns[2:16])     # Default selection is all columns from index 2 onwards
        
        # Allow user to select multiple causes
        selected_causes = st.sidebar.multiselect("Select Causes", options=options, default=default)
        
        # Filter data for selected state and causes
        filtered_data = df[df['Area_Name'] == selected_state][['Year', 'Area_Name'] + selected_causes]
        
        # Reshape data for plotting (melt)
        df_reset = pd.melt(filtered_data, id_vars=['Year', 'Area_Name'], value_vars=selected_causes, 
                        var_name='Cause', value_name='Count')
        
        # Create grouped bar chart using Plotly Express
        fig_grouped_bar = px.bar(df_reset, x='Year', y='Count', color='Cause', barmode='group',
                                title=f'Number of Murders by Cause in {selected_state}',
                                labels={'Count': 'Number of Murders', 'Cause': 'Murder Cause'})
        

        fig_grouped_bar.update_layout(xaxis_title='Year', yaxis_title='Number of Murders')
        st.plotly_chart(fig_grouped_bar)

     elif selected_option == "Stacked Bar Chart by Murder Cause":
        df_proportions = df.melt(id_vars=['Year', 'Area_Name'], value_vars=df.columns[2:], var_name='Cause', value_name='Count')
        df_proportions['Proportion'] = df_proportions['Count'] / df_proportions.groupby('Year')['Count'].transform('sum')
        fig_stacked_bar = px.bar(df_proportions, x='Year', y='Proportion', color='Cause', barmode='stack',
                                title='Proportions of Different Murder Causes (Stacked Bar Chart)',
                                labels={'Proportion': 'Proportion', 'Cause': 'Murder Cause'})
        st.plotly_chart(fig_stacked_bar)

     elif selected_option == "Pie Chart of Murder Causes for 2005":
        df_2005 = df[df['Year'] == 2005].drop(columns=['Year', 'Area_Name', 'Murder_Cause_Total']).sum().reset_index()
        df_2005.columns = ['Cause', 'Count']
        fig_pie_2005 = px.pie(df_2005, names='Cause', values='Count', title='Murder Causes Distribution for 2005 (Pie Chart)', hole=0.3)
        st.plotly_chart(fig_pie_2005)
     elif selected_option == "Scatter plot of Murder Causes Over Time":
        df_reset = df.melt(id_vars=['Year', 'Area_Name'], value_vars=df.columns[16:], var_name='Cause', value_name='Count')
        fig_scatter = px.scatter(df_reset, x='Year', y='Count', color='Cause', title='Trends of Murder Causes Over Time (Scatter Plot)',
                                labels={'Count': 'Number of Murders', 'Cause': 'Murder Cause'})
        
        fig_scatter.update_layout(xaxis_title='Year', yaxis_title='Number of Murders')
        
        st.plotly_chart(fig_scatter)
     elif selected_option == "Heat Map of Murder Causes":
        heatmap_data = df.pivot_table(index='Area_Name', columns='Year', values='Murder_Cause_Total', fill_value=0)
        fig_heatmap = px.imshow(heatmap_data, labels=dict(x='Year', y='Region', color='Murder Cause Total'),
                                title='Heat Map of Different Murder Causes', color_continuous_scale='YlGnBu')
        st.plotly_chart(fig_heatmap)
     elif selected_option == "Total Murder Causes Comparison":
        murder_causes_columns = [
            'Murder_Cause_By_TerroristExtremist',
            'Murder_Cause_Casteism',
            'Murder_Cause_Class_Conflict',
            'Murder_Cause_Communalism',
            'Murder_Cause_Dowry',
            'Murder_Cause_For_Political_reason',
            'Murder_Cause_Gain',
            'Murder_Cause_Love_AffairsSexual_Relations',
            'Murder_Cause_Lunacy',
            'Murder_Cause_Other_Causes_or_Motives',
            'Murder_Cause_Personal_Vendetta_or_Enmity',
            'Murder_Cause_Property_Dispute',
            'Murder_Cause_Witchcraft'
                                              ]

        total_murders = df[murder_causes_columns].sum().sort_values(ascending=False).reset_index()
        total_murders.columns = ['Murder_Cause', 'Total_Murders']

        fig = px.bar(total_murders, x='Murder_Cause', y='Total_Murders',
                    title='Total Murders by Cause',
                    labels={'Murder_Cause': 'Cause of Murder', 'Total_Murders': 'Total Murders'},
                    text='Total_Murders', 
                    color='Total_Murders',  
                    color_continuous_scale='Viridis')  
        fig.update_layout(
            xaxis_title='Cause of Murder',
            yaxis_title='Total Murders',
            xaxis_tickangle=-45,  
            title_x=0.5,  
            title_y=0.95  
        )
        fig.show()
    else:
        st.write("Please select a valid option from the sidebar.") 
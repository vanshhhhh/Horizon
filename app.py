import pandas as pd
import streamlit as st
@st.cache(show_spinner=False)
def getData1():
    #Solar radio flux - https://www.spaceweather.gc.ca/forecast-prevision/solar-solaire/solarflux/sx-5-en.php
    monthlyAvg = pd.read_html('https://www.spaceweather.gc.ca/forecast-prevision/solar-solaire/solarflux/sx-5-mavg-en.php')[0]
    monthlyAvg['Date'] = pd.to_datetime(monthlyAvg[['Year', 'Month']].assign(DAY=1))
    monthlyAvg = monthlyAvg.drop(['Year', 'Month'], axis=1)
    monthlyAvg = monthlyAvg.set_index('Date')
    return monthlyAvg
@st.cache(show_spinner=False)
def getData2():
    rotationalAvg = pd.read_html('https://www.spaceweather.gc.ca/forecast-prevision/solar-solaire/solarflux/sx-5-ravg-en.php')[0]
    return rotationalAvg
@st.cache(show_spinner=False)
def getData3():
    dailyFluxValues = pd.read_html('https://www.spaceweather.gc.ca/forecast-prevision/solar-solaire/solarflux/sx-5-flux-en.php')[0]
    dailyFluxValues = dailyFluxValues.set_index('Date')
    dailyFluxValues = dailyFluxValues.drop(['Time', 'Julian day'], axis = 1)
    return dailyFluxValues
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            </style>
            """
st.set_page_config(
    page_title="Horizon",
    page_icon = ":rocket:"
)
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
st.sidebar.title("Horizon")
st.sidebar.image("./assets/images/nasa-logo.png", use_column_width=True)
rad = st.sidebar.radio('Navigation Menu',['Home', 'About'])
if rad =='About':
    st.title("About")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.subheader("Team - Blue Moon")
        st.image("./assets/images/team-logo.jpg", use_column_width=True)
    st.write("This project was created by a team of 2 students - [Vansh Sharma](https://www.linkedin.com/in/vanshsharma10/) and [Bhavy Bansal](https://www.linkedin.com/in/bhavybansal24/) from the Manipal University Jaipur, India for the [NASA Space Apps Challenge 2022](https://www.spaceappschallenge.org/). Make sure to give this a star on [GitHub](https://github.com/vanshhhhh/Horizon).")
if rad == 'Home':
    st.title("Solar Flux Analysis")
    options = st.radio('Select data type', ['Monthly Average', 'Rotational Average', 'Daily Flux Values'], horizontal=True)
    details = """
            **Daily flux** values are the radio emission from the Sun at a wavelength of 10.7 centimetres recorded daily. Values prior to October 28, 2004 are no longer available directly from the web site. They continue to be available through our FTP server. Please contact us using the [Contact Us - Email Form](http://contact-contactez.nrcan-rncan.gc.ca/index.cfm?lang=en&sid=7&context=hazards) for more information.
                
            **Monthly averages** are the radio emission from the Sun at a wavelength of 10.7 centimetres averaged over the month. The units are in solar flux units (1 sfu = 10-22.m-2.Hz-1).
                
            **Rotational averages** are the radio emission from the Sun at a wavelength of 10.7 centimetres averaged over the Carrington Rotation. The units are in solar flux units (1 sfu = 10-22.m-2.Hz-1). The Carrington Rotation Number is the number of times the Sun has rotated since 9th November, 1853. The rotation period is roughly 27 days.
                
            More explanation can be found at the [About the Data](https://www.spaceweather.gc.ca/solarflux/sx-3-en.php) page."""
    st.subheader(options)
    if options == "Monthly Average":
        monthlyAvg = getData1()
        with st.expander("Details and Customization"):
            st.write(details)
            initialYear = monthlyAvg.index[0]
            finalYear = monthlyAvg.index[-1]
            st.write("The graph below is displaying data from **{}** to **{}**".format(str(initialYear).partition("-")[0], str(finalYear).partition("-")[0]))
            selectColumns1 = st.multiselect('Customize inputs', monthlyAvg.columns)
        try:
            if selectColumns1 == []:
                st.line_chart(monthlyAvg[monthlyAvg.columns])
            else:
                st.line_chart(monthlyAvg[selectColumns1])
        except Exception as e:
            st.warning(e)
    if options == "Rotational Average":
        rotationalAvg = getData2()
        with st.expander("Details and Customization"):
            st.write(details)
            selectColumns2 = st.multiselect('Customize inputs', rotationalAvg.columns)
        try:
            if selectColumns2 == []:
                st.line_chart(rotationalAvg[rotationalAvg.columns])
            else:
                st.line_chart(rotationalAvg[selectColumns2])
        except Exception as e:
            st.warning(e)
    if options == "Daily Flux Values":
        dailyFluxValues = getData3()
        with st.expander("Details and Customization"):
            st.write(details)
            selectColumns3 = st.multiselect('Customize inputs', dailyFluxValues.columns)
        try:
            if selectColumns3 == []:
                st.line_chart(dailyFluxValues[dailyFluxValues.columns])
            else:
                st.line_chart(dailyFluxValues[selectColumns3])
        except Exception as e:
            st.warning(e)
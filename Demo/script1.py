from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    import yfinance as yf
    from bokeh.plotting import figure, show, output_file 
    from bokeh.embed import components
    from bokeh.resources import CDN

    # Definir las fechas de inicio y fin
    start = '2015-11-01'
    end = '2016-03-10'

    # Descargar datos
    df = yf.download('AAPL', start=start, end=end)

    # Mostrar los datos
    print(df)
    def in_dec(close, open):
        if close > open:
            value = "Increase"
        elif close < open:
            value = "Decrease"
        else:
            value = "Equal" 
        return value

    df["Status"] = [in_dec(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Open+df.Close)/2
    df['Height']=abs(df.Close-df.Open)

    df
    p= figure(x_axis_type='datetime', width=1000, height=300, sizing_mode = 'scale_width')
    p.title = "Candlestick Chart"
    p.grid.grid_line_alpha=0.3

    hours_12 = 12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color='Black')

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
        hours_12, df.Height[df.Status=="Increase"], fill_color='#52BE80', line_color='black')
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
        hours_12, df.Height[df.Status=="Decrease"], fill_color='#E74C3C', line_color='black')

    #output_file("CS.html")
    #show(p)

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = 'https://cdn.pydata.org/bokeh/relese/bokeh-0.11.1.min.css'

    return render_template("plot.html",
                           
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js
    )
    
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
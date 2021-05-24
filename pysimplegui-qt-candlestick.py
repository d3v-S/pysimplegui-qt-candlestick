#from stock_datasource import DataSource
import PySimpleGUIQt as sg

##########
# Candles:
##########

class CandleStick:
    def __init__(self, o, c, h, l, volume=None, time=None):
        self.open = float(o)
        self.close = float(c)
        self.high = float(h)
        self.low = float(l)
        self.volume = float(volume)
        self.time = time
        self.color = None
        self.dir = None
        self.body_percent = None
        self.body = None
        self.up_wick = None
        self.down_wick = None
        self.body_width = 2
        self.plotted_figure = None # list of any figure that is used to plot this graph.
        self.colorOfCandle()
        self.typeOfCandle()

    
    def colorOfCandle(self):
        if (self.open > self.close):
            self.color = "Red"
            self.dir = False
        else:
            self.color = "Green"
            self.dir = True
    
    def typeOfCandle(self):
        if (self.dir):
            self.body = (self.close - self.open)
            self.up_wick = (self.high - self.close)
            self.down_wick =(self.open - self.low)
        else:
            self.body = (self.open - self.close)
            self.up_wick = (self.high - self.open)
            self.down_wick = (self.close - self.low)
        
        if (self.open != self.close):
            self.body_percent = (self.high - self.low)/abs(self.open - self.close)
        else:
            self.body_percent = 1
    
    def addFigures(self, list_fig):
        self.plotted_figure = list_fig

    def delFigures(self):
        self.plotted_figure = None


    # input = json_arr === [{"high", "low"", .... }]
    # output = [candle1, candle2...]
    # keys = ["Open", "Close", "High", "Low", "Volume", "Date"]
    @classmethod
    def getListOfCandlesSticks(cls, arr_json):
        list_candles = []
        for item in arr_json:
            c = CandleStick(item['Open'], item["Close"], item["High"], item["Low"], volume = item["Volume"], time= item["Date"])
            list_candles.append(c)
        return list_candles


    # used to plot on Pysimplegui
    # on the given Graph(Canvas) element from pysimplegui
    @classmethod
    def sgPlotCandle(cls, candle, graph, x, y, price_per_pixel):
        down_wick = candle.down_wick / price_per_pixel
        up_wick = candle.up_wick / price_per_pixel
        body = candle.body / price_per_pixel
        fig_down_wick = graph.draw_line((x, y), (x, y + down_wick), color = candle.color)
        fig_body_wick = graph.draw_rectangle((x - candle.body_width, y + down_wick), ( x + candle.body_width, y + down_wick + body), line_color = candle.color)
        fig_up_wick = graph.draw_line((x, y + down_wick + body), (x, y +  down_wick + body + up_wick), color = candle.color)
        #candle.addFigures([fig_body_wick, fig_down_wick, fig_up_wick])


#####################
# CandleStick Charts: -> PySimpleGui, plotting.
##################### 
class CandleStickCharts:

    # input = list of candles:
    # output = max and min price.
    @classmethod
    def __getPriceRangeFromCandles(cls, arr_candles):
        min_price = 999999999
        max_price = 0
        for candle in arr_candles:
            if (candle.low < min_price):
                min_price = candle.low
            if (candle.high > max_price):
                max_price = candle.high
        return (min_price, max_price)

    def __init__(self, graph, arr_candles, canvas_loc, num_candles = 200):
        self.num_candles = num_candles
        if len(arr_candles) < num_candles:
            self.num_candles = len(arr_candles)
        self.graph = graph
        self.arr_candles = arr_candles
        self.startx = canvas_loc[0][0]
        self.starty = canvas_loc[0][1]
        self.endx = canvas_loc[1][0]
        self.endy = canvas_loc[1][1]
        self.min_price = None
        self.max_price = None
        self.dist_bw_candle = 4
        self.price_per_pixel = self.getPricePerPixel()
    
    def getPricePerPixel(self):
        price_range = CandleStickCharts.__getPriceRangeFromCandles(self.arr_candles[:self.num_candles])
        self.min_price = price_range[0]
        self.max_price = price_range[1]
        return (self.max_price - self.min_price) / (self.endy - self.starty)

    # plot chart for pysimplegui
    def sgPlotChart(self):
        print("Plotting.. " + str(self.num_candles))
        x = self.endx - 10
        y = self.starty
        for i in range(0, self.num_candles):
            candle = self.arr_candles[i]
            y = (1/self.price_per_pixel) * (candle.low - self.min_price)
            CandleStick.sgPlotCandle(self.arr_candles[i],self.graph, x, y, self.price_per_pixel)
            x = x - candle.body_width - self.dist_bw_candle




#arr_json = DataSource.getDataFromSource("et", timeframe=5, start="2021-04-28", end="2021-04-28")
# arr_json = [ {Date:, High:, Low:, Open:, CLose:},  {}, ]


#arr_json1 = DataSource.mergeDataIntoLargerTimeFrame(DataSource.getDataFromSource("mc", start="2021-04-28", end="2021-04-28"), 1, 5, "2021-04-28 09:15", "2021-04-28 15:25" )

#print(arr_json)
#print(arr_json1)

layout = [[sg.Graph(canvas_size=(800, 400), graph_bottom_left=(0, 0), graph_top_right=(800, 400), background_color='black', enable_events=True, key='graph')]]
window = sg.Window('Graph test', layout, finalize=True).finalize()
graph = window['graph']

# cc = CandleStickCharts(graph, CandleStick.getListOfCandlesSticks(arr_json), ((0,0),(800,400)))
# cc.sgPlotChart()
#
# cc1 = CandleStickCharts(graph, CandleStick.getListOfCandlesSticks(arr_json1), ((0,0),(800,400)))
# cc1.sgPlotChart()

# window.read()






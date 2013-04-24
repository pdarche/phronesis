var app = app || {};

app.LineChartWithContext = Backbone.View.extend({

    initialize : function() {

        this.renderChart( this )

    },

    render : function() {


    },

    events : {


    },

    renderChart : function( self ) {

        var adj = $('.active-adj').html(),
            accent = accents[adj],
            data = this.model

        this.$el.empty()

        var margin = {top: 10, right: 10, bottom: 100, left: 40},
            margin2 = {top: 450, right: 10, bottom: 20, left: 40},
            width = this.$el.width() - margin.left - margin.right,
            height = this.$el.height() - margin.top - margin.bottom,
            height2 = this.$el.height() - margin2.top - margin2.bottom - 20;

        var parseDate = d3.time.format("%b %Y").parse;

        var brushed = function(){
              console.log("firing brush function")
              x.domain(brush.empty() ? x2.domain() : brush.extent());
              focus.select("path").attr("d", line);
              focus.select(".x.axis").call(xAxis);
        }

        var x = d3.time.scale().range([0, width]),
            x2 = d3.time.scale().range([0, width]),
            y = d3.scale.linear().range([height, 0]),
            y2 = d3.scale.linear().range([height2, 0]);

        var xAxis = d3.svg.axis().scale(x).orient("bottom"),
            xAxis2 = d3.svg.axis().scale(x2).orient("bottom"),
            yAxis = d3.svg.axis().scale(y).orient("left");

        var brush = d3.svg.brush()
            .x(x2)
            .on("brush", brushed);

        var line = d3.svg.line()
                .interpolate("cardinal")
                .x(function(d) {
                    var date = new Date(d.date * 1000)
                    return x(date)
                    // return x(d.date)
                })
                .y(function(d) { return y(d.value) })

        var line2 = d3.svg.line()
                .interpolate("cardinal")
                .x(function(d) {
                    // return x2(d.date)
                    var date = new Date(d.date * 1000)
                    return x2(date)
                    })
                .y(function(d) { return y2(d.value) })

        var svg = d3.select("#vis_container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        svg.append("defs").append("clipPath")
            .attr("id", "clip")
          .append("rect")
            .attr("width", width)
            .attr("height", height);

        var focus = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var context = svg.append("g")
            .attr("transform", "translate(" + margin2.left + "," + ( margin2.top + 15 ) + ")");


          x.domain(d3.extent(data.map(function(d) { return d.date * 1000; })));
          y.domain([0, d3.max(data.map(function(d) { return d.value; }))]);
          x2.domain(x.domain());
          y2.domain(y.domain());

          focus.append("path")
              .datum(data)
              .attr("clip-path", "url(#clip)")
              .attr("d", line)
              .style('stroke', accent)

          focus.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);

          focus.append("g")
              .attr("class", "y axis")
              .call(yAxis);

          context.append("path")
              .datum(data)
              .attr("d", line2)
              .style('stroke', accent)

          context.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + ( height2 + 20 ) + ")")
              .call(xAxis2);

          context.append("g")
              .attr("class", "x brush")
              .call(brush)
            .selectAll("rect")
              .attr("y", -5)
              .attr("height", height2 + 22);


    },

    prepData : function( data ){

        var data = [],
            dates = [],
            vals = [],
            dataType = this.getDataType(),
            x, y, title

        _.each( this.model.data, function(obj){

            var datum = { x: obj.created_at, y : obj[dataType] }
            vals.push(obj[dataType])
            x = "dates",
            y = "minutes",
            title = "Minutes Very Active"

            data.push(datum)
            dates.push(obj.created_at)

        })

        var mean = j$(vals).mean(),
            median = j$(vals).median(),
            mode = j$(vals).mode(),
            sd = j$(vals).stdev()

        return { 
            data : data,
            dates : dates,
            vals : vals,
            mean : mean,
            median : median,
            mode : mode,
            sd : sd,
            xAxis : x,
            yAxis : y,
            title : title
        }

    },

    getDataInfo : function(){

    },

    changeDataSource : function( ev ) {
        var self = this

        $('.data-source').removeClass('data-source')
        $(ev.target).addClass('data-source')
        self.renderChart( self )

    },


    removeChart : function(){

        this.$el.remove()

    }





})
var app = app || {};

app.Histogram = Backbone.View.extend({
    tagName : 'div',
    className : 'histogram-container',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/histogram.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.renderChart( self )

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.append( template )

    },

    events : {

        "click .destroy" : "removeChart",
        "click .record-attribute" : "changeDataSource",

    },

    renderChart : function( self ) {

        var adj = $('.active-adj').html(),
            accent = accents[adj]

        var returnedData = this.prepData(),
            values = returnedData.vals

        var min = d3.min(values),
            max = d3.max(values)

        console.log(min)

        var classSelector = '.histogram'

        // A formatter for counts.
        var formatCount = d3.format(",.0f");

        d3.select(classSelector).select('svg').remove()

        var margin = {top: 10, right: 20, bottom: 20, left: 20},
            width = this.$el.width() - margin.left - margin.right,
            height = this.$el.height() - 50 - margin.top - margin.bottom

        var x = d3.scale.linear()
            .domain([0, max])
            .range([0, width]);

        // Generate a histogram using twenty uniformly-spaced bins.
        var data = d3.layout.histogram()
            .bins(x.ticks(20))
            (values);

        var y = d3.scale.linear()
            .domain([0, d3.max(data, function(d) { return d.y; })])
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var svg = d3.select(classSelector).select('.vis-container').append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var bar = svg.selectAll(".bar")
            .data(data)
          .enter().append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

        bar.append("rect")
            .attr("x", 1)
            .attr("width", x(data[0].dx) - 1)
            .attr("height", function(d) { return height - y(d.y); })
            .style("fill" , accent)
            .style("fill-opacity", .8)

        bar.append("text")
            .attr("dy", ".75em")
            .attr("y", function(d){
                var y;
                d.y < 5 ? y = -16 : y = 6
                return y
            })
            .attr("x", x(data[0].dx) / 2)
            .attr("text-anchor", "middle")
            .text(function(d) { return formatCount(d.y); });

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    },


    prepData : function( selected ){

        var vals = [],
            dataType = this.getDataType(),
            x, y, title

        _.each( this.model.data, function(obj){

            if ( dataType === "mins_very_active" ){
                vals.push(obj[dataType])
                x = "dates",
                y = "minutes",
                title = "Minutes Very Active"
            } else if ( dataType === "power" ) {
                var powerUsage = Math.floor(Math.random() * 2000) + 3000
                vals.push(powerUsage)
                x = "dates",
                y = "watts",
                title = "Average Watts Per Day"
            }

        })

        var mean = j$(vals).mean(),
            median = j$(vals).median(),
            mode = j$(vals).mode(),
            sd = j$(vals).stdev()

        return {        
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

    getDataType : function(){

        var activeAdj = $('.active-adj').html()

        var dataType

        switch(activeAdj){
            case "healthy":
                console.log("steps")
                dataType = "mins_very_active"
                break
            case "sustainable":
                dataType = "power" 
                console.log("power")
                break
            case "educated":
                dataType = "books"
                console.log("books")
                break
        }

        return dataType
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
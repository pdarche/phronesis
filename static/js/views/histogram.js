var app = app || {};

app.Histogram = Backbone.View.extend({
    tagName : 'div',
    className : 'histogram-container',
    id : undefined,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/histogram.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.$el.attr( 'id', 'histogram_' + $('.histogram-container').length )
                var idSelector = '#' + self.$el.attr('id') 

                $(idSelector).draggable().resizable({
                    stop : function() {
                        self.renderChart( self )
                    }
                })

                self.renderChart( self )

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var attributes = []

        for ( attr in categoryAttributes[this.model.attribute] ) {
             attributes.push({ 
                title : attr, 
                id : categoryAttributes[this.model.attribute][attr] 
            })
        }

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "attribute" : attributes } ) )

        if ( this.model.attribute === "physicalActivity"){
            $('#steps').addClass('data-source')
        } else if ( this.model.attribute === "sleep"){
            $('#total_z').addClass('data-source')
        } else {
            $('#calories').addClass('data-source')
        }

    },

    events : {

        "click .destroy" : "removeChart",
        "click .record-attribute" : "changeDataSource",

    },

    renderChart : function( self ) {

        // Generate an Irwin–Hall distribution of 10 random variables.
        // var values = d3.range(1000).map(d3.random.irwinHall(10));
        var values = this.prepData()

        var min = d3.min(values),
            max = d3.max(values)

        var idSelector = '#' + this.$el.attr('id')

        // A formatter for counts.
        var formatCount = d3.format(",.0f");

        d3.select(idSelector).select('svg').remove()

        var margin = {top: 10, right: 30, bottom: 30, left: 30},
            width = this.$el.width() - margin.left - margin.right,
            height = this.$el.height() - $('.destroy').height() - 50 - margin.top - margin.bottom

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

        var svg = d3.select(idSelector).append("svg")
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
            // .style("fill" : "steelblue")   

        bar.append("text")
            .attr("dy", ".75em")
            .attr("y", 6)
            .attr("x", x(data[0].dx) / 2)
            .attr("text-anchor", "middle")
            .text(function(d) { return formatCount(d.y); });

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    },

    prepData : function(){

        var data = [],
            selected = $('.data-source').attr('id')

            console.log("the selected attribute is", selected)

        _.each( this.model.records, function(obj){

            data.push(obj[selected])

        })

        return data

    },

    changeDataSource : function( ev ) {
        var self = this

        $('.data-source').removeClass('data-source')
        $(ev.target).addClass('data-source')
        self.renderChart( self )

        // $.when( $('.data-source').removeClass('data-source'))
        // .done(
        //     function(){
        //         $(ev.target).addClass('data-source')
        //         console.log("the target is ", ev.target)
        //         self.renderChart( self )
        //     }
        // )

    },

    removeChart : function(){

        this.$el.remove()

    }

})
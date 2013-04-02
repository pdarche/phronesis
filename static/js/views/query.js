var app = app || {};

app.QueryCollection = Backbone.View.extend({
	tagName : 'div',
	className : 'query-collection',
	id : undefined,

    initialize: function(){

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/queryCollection.handlebars', function(tmpl){
                self.template = tmpl
                self.render( tmpl )
                self.$el.attr('id', 'query_collection_' + $('.query-collection').length) 
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function( tmpl ) {

        var self = this

        var source = $(tmpl).html()
        var template = Handlebars.compile( source )
        this.$el.html( template(self.model) )

        $('.query-collection').draggable({
            revert : true
        })

        this.$el.data('collection-data', this.model)

    }

});

app.QueryView = Backbone.View.extend({
    
    startDate : undefined,
    endDate : undefined,

    initialize: function(){

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/queryContainer.handlebars', function(tmpl){
                self.template = tmpl
                self.render( tmpl )

                $.proxy(self.bindSlider(), self)

                // $('#query_container').draggable()

                $('.chart-type-container').droppable({
                	accept : '.query-collection',
                    hoverClass : 'chart-type-container-hover',
                    drop : function(ev, ui) {

                        var draggableSelector = '#' + ui.draggable.attr('id');
                        var model = $(draggableSelector).data('collection-data')
                        self.createChart( model, $(this).attr('id') )
                    	self.toggleContainer()

                    }
                })

            })

        } else {

            console.log("gots the template")

        }

    },

    render: function( tmpl ){

        $('body').append('<div id="chart_container"></div>')

        var source = $(tmpl).html()
        var template = Handlebars.compile( source )
        $('body').append( template )

        // var pad = 80,
        //     w = window.innerWidth - (2*pad),
        //     h = window.innerHeight - (2*pad)

        // var linedata = function( w, numLines ){
            
        //     var sep = w/numLines,
        //         data = []

        //     for ( var i = 1; i < numLines; i++ ) {
        //         data.push( (sep * i) )
        //     } 

        //     return data
        // }

        // var vis = d3.select('#chart_container')
        //     .append('svg')
        //     .attr('width', window.innerWidth)
        //     .attr('height', window.innerHeight)
        //     .append('svg:g')
        //         .attr('transform', 'translate(' + (w/2 + pad) + ',' + pad + ')')

        // vis.append('rect').attr('width', w/2).attr('height', h)

        // vis.selectAll('line.xGrid')
        //     .data(linedata(w/2,30))
        //   .enter().append('line')
        //     .attr('class', 'xGrid')
        //     .attr('x1', function(d) { return d })
        //     .attr('x2', function(d) { return d })
        //     .attr('y1', 0)
        //     .attr('y2', h)

        // vis.selectAll('line.yGrid')
        //     .data(linedata(h,30))
        //   .enter().append('line')
        //     .attr('class', 'yGrid')
        //     .attr('y1', function(d) { return d })
        //     .attr('y2', function(d) { return d })
        //     .attr('x1', 0)
        //     .attr('x2', w/2)

        // vis.append('text').text('Drag Records Here')
        //     .attr('font-size', '50px')
        //     .attr('x', function(){
        //         var offset = w/4 - d3.select('text').node().getComputedTextLength()/2
        //         return offset
        //     })
        //     .attr('y', h/2)
        //     .style('fill', 'gray')
        //     .on('mouseover', function(){
        //         d3.select('rect').style('stroke', 'white')
        //     })
        //     .on('mouseout', function(){
        //         d3.select('rect').style('stroke', 'grey')
        //     })

        // d3.select('body').insert('div')
        //     .style('fixed','top')
        //     .style('height','100px')
        //     .style('background-color', 'rgba(255,255,255,.6)')
        //     .style('border-bottom', '1px solid white')
        //     .style('box-shadow', '0px 2px 10px gray')

    },
    
    events : {

        "click .category" : "chooseCategory",
        "change select" : "getRecords",
        "dblclick #query_container" : "toggleContainer"
        // "click .record-attribute" : "chooseAttribute"

    },

    formatDate : function( date ){

        var day = date.getDate(),
            month = date.getMonth(),
            year = date.getFullYear()

        return ( month + 1) + '/' + day + '/' + year 

    },

    chooseCategory : function(ev){

        var self = this

        $('.chosen').removeClass('chosen')
        $(ev.target).addClass('chosen')

        var category = $('.chosen').attr('id')

        $.when( 
            $.getJSON('/v1/data/pdarche/body/' + category +'?limit=1&order_by=created_at__asc'),
            $.getJSON('/v1/data/pdarche/body/' + category +'?limit=1&order_by=created_at__desc')
         )
        .done(
            function(start, end){
                var s = start[0][0].created_at,
                    e = end[0][0].created_at

                $("#range_container")
                    .slider('option', 'min', s)
                    .slider('option', 'max', e)
                    .slider('values', [s, e])
            
                var attributes = Object.keys(start[0][0])

            }
        )

    },

    bindSlider : function() {

        var self = this

        $("#range_container").slider({
            range : true,
            min : 0,
            max : 100,
            values : [75,100],
            slide: function( event, ui ) {

                self.startDate = ui.values[0]
                self.endDate = ui.values[1]

                var startDate = new Date(ui.values[0] * 1000),
                    endDate = new Date(ui.values[1] * 1000)

                $('#slider_start_date').html( self.formatDate(startDate))
                $('#slider_end_date').html( self.formatDate(endDate))

            }
        });

    },

    toggleContainer : function() {

    	console.log("dblclicking", pos)

    	var pos = $('#query_container').css('left')
    	pos === "0px" ? $('#query_container').animate({ left : '-=350px' }) : $('#query_container').animate({ left : '+=350px' })

    },

    getRecords : function(){

        var category = $('.chosen').attr('id'),
            limit = $('#limit input').val(),
            order_by = 'created_at__' + $('#ordering option:selected').val(),
            dateValues = $('#range_container').slider('values'),
            self = this

        if ( category === undefined ) {
            console.log("no category selected")
            return 
        }

        var url = '/v1/data/pdarche/body/' + category + '?' + this.checkDefined('order_by', order_by)
            url += this.checkDefined('limit', limit, "&")
            url += '&created_at__gte=' + dateValues[0] + '&created_at__lte=' + dateValues[1]

        $.getJSON(url, function(data){
            
            self.createRecords( data )

        })

    },

    checkDefined : function(key,val,amp) {

        amp === undefined ? amp = "" : null

        if ( val === undefined ) {
            return ""
        } else {
            return amp+key + '=' + val
        }

    },

    createRecords : function( collection ){

        // _.each( collection, function(c){ console.log(c) }) 

        var startDate = $('#slider_start_date').html(),
            endDate = $('#slider_end_date').html(),
            category = $('.chosen').html(),
            attribute = $('.chosen').attr('id')


        var model = {
            category : category,
            attribute : attribute,
            startDate : startDate,
            endDate : endDate,
            recordCount : collection.length,
            records : collection
        }

        var collection = new app.QueryCollection({
                model : model
            })

        $('#query_container').append( collection.el )

    },

    createChart : function( model, chartType ){

    	console.log(chartType)

        switch ( chartType ){
        	case "line_chart" :
        		var line = new app.LineChart({ model : model })
        		$('body').append( line.el )
        		break;
        	case "scatter_plot" :
        		// var scatterplot
        		console.log("scatter")
        		break;
        	case "pie_chart" :
        		console.log("pie")
        		// car pie chart
        		break;
        	case "histogram" :
        		console.log("hist")
        		// var histogram 
        		break;
        }

    }

});


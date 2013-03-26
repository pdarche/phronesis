var app = app || {};

app.QueryView = Backbone.View.extend({
    
    initialize: function(){

        this.render();

    },

    render: function(){

        // $.when( $.get('/static/js/templates/queryView.handlebars') )
        // .done( function(data){ 
            
        //     var source = $(data).html()
        //     var template = Handlebars.compile( source )
        //     $('body').append( template )

        // })

        $('body').append('<div id="chart_container"></div>')

        var pad = 80,
            w = window.innerWidth - (2*pad),
            h = window.innerHeight - (2*pad)

        var linedata = function( w, numLines ){
            
            var sep = w/numLines,
                data = []

            for ( var i = 1; i < numLines; i++ ) {
                data.push( (sep * i) )
            } 

            return data
        }

        var vis = d3.select('#chart_container')
            .append('svg')
            .attr('width', w + (2*pad))
            .attr('height', h + (2*pad))
            .append('svg:g')
                .attr('transform', 'translate(' + pad + ',' + pad + ')')

        vis.append('rect').attr('width', w).attr('height', h)

        vis.selectAll('line.xGrid')
            .data(linedata(w,30))
          .enter().append('line')
            .attr('class', 'xGrid')
            .attr('x1', function(d) { return d })
            .attr('x2', function(d) { return d })
            .attr('y1', 0)
            .attr('y2', h)

        vis.selectAll('line.yGrid')
            .data(linedata(h,30))
          .enter().append('line')
            .attr('class', 'yGrid')
            .attr('y1', function(d) { return d })
            .attr('y2', function(d) { return d })
            .attr('x1', 0)
            .attr('x2', w)

        vis.append('text').text('Drag Records Here')
            .attr('x', 50)
            .attr('y', h/2)
            .attr('font-size', '50px')
            .on('mouseover', function(){
                d3.select('rect').style('stroke', 'white')
            })
            .on('mouseout', function(){
                d3.select('rect').style('stroke', 'grey')
            })

    },
    
    events : {

        // "click .attribute" : "clicky"

    }

});

var app = app || {};

app.DescriptiveStats = Backbone.View.extend({
    tagName : 'div',
    className : 'histogram-container',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/descriptiveStats.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
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


    },


    prepData : function( selected ){


    },

    getDataType : function(){


    },

    changeDataSource : function( ev ) {


    },

    removeChart : function(){


    }

})
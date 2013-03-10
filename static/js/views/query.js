QueryView = Backbone.View.extend({
    
    initialize: function(){
        this.render();
    },

    render: function(){

        $.when( $.get('/static/js/templates/queryView.handlebars') )
        .done( function(data){ 
            
            var source = $(data).html()
            var template = Handlebars.compile( source )
            $('body').append( template )

        })

    },
    
    events : {

        "click .attribute" : "clicky"

    },

    clicky : function(){

        

    }

});

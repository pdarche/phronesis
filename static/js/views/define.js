var app = app || {};

app.DefineView = Backbone.View.extend({
    // tagName : 'div',
    // className : 'define-container',

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/defineView.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.transitionIn()
            })

        } else {

            self.render()

        }

    },

    render : function() {

        console.log("rendering")

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "adjectives" : adjectives } ) )

    },

    transitionIn : function(){

        $('#define_instructions').removeClass('hidden-top')
        $('.adjective').removeClass('hidden-left')
        $('.top-adj').removeClass('hidden-left')

    },

    events : {

        "click .adjective" : "toggleAdjective"

    },

    toggleAdjective : function(ev){

        var self = this

        $(ev.target).hasClass('chosen-adj') ? $(ev.target).removeClass('chosen-adj') : $(ev.target).addClass('chosen-adj')

        if ( $('.chosen-adj').length === 3 ){

            $('.adjective').not('.chosen-adj').addClass('hidden-left')
            self.expandChosen()
        
        }

    },

    expandChosen : function(){

        $('.chosen-adj').addClass('enlarged')
        $('.adjective').not('.chosen-adj').remove()
        //unbind adjective choice

    }

})
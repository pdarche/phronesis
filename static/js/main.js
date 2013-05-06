
$(document).ready(function(){

			var AppRouter = Backbone.Router.extend({
				routes: {
					"": "index",
					"nutrition" : "nutrition",
					"landingpage" : "landingpage",
					"query" : "query",
					"define" : "define",
					"what" : "what",
					"why" : "why",
					"how" : "how",
					"profile" : "profile",
					"addTrackers" : "addTrackers"
				}
			});

			$('.nav-element').click(function(){
				var view = $(this).attr('id')
				window.location.hash = view
				$('.active-view').removeClass('active-view')
				$(this).addClass('active-view')
			})

			$('.nav-adjective').click(function(){

				var currentAdj = $('.active-adj').html() + '-accent'
				
				if ( !$(this).hasClass('active-adj') ){

					var adjAccent = $(this).html() + '-accent'
					$('.active-adj').removeClass(currentAdj + ' active-adj')
					$(this).addClass(adjAccent + ' active-adj')

				}

				if ( window.location.hash === '#what' ){
				

				
				} else if ( window.location.hash === '#why') {

					checkUserStatus()

					// $.when( 
					// 	$.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000&created_at__lte=1365375284')
					//  )
					//  .done( function(data){
					//  	var why = new app.GridView({ el : $('#content_container'), model : data })
					//  })

				} else {					
	            	var activeAdj = $('.active-adj').html(),
	                actions = new app.ActionsView({
	                    el : $('#action_list'),
	                    model : adj[activeAdj]
	                })
				}

			})
			
    		// Initiate the router
		    var app_router = new AppRouter;

		    app_router.on('route:index', function() {
		        
		        $('#content_container').undelegate()
				var login = new app.Login({ el : $('#content_container') })

		    })

		    app_router.on('route:nutrition', function() {

		    	$('body').append("<div id='meals_container'></div>")
				var nutrition_view = new app.NutritionView({ el: $('#meals_container') });

		    })

		    app_router.on('route:landingpage', function(){

		    	$('#content_container').undelegate()
		    	var landingpage = new app.LandingPage({ el : $('#content_container')})

		    })

		    app_router.on('route:query', function(){

		    	$('#content_container').undelegate()
		    	var query = new app.QueryView({ el : $('#content_container')})

		    })

			app_router.on('route:define', function(){

				$('#content_container').undelegate()
		    	var define = new app.DefineView({ el : $('#content_container')})

		    })

		    app_router.on('route:why', function(){

		    	checkUserStatus()

		    	// var why = new app.GridView({ el : $('#content_container')})
	    		$.when(
					$.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000&created_at__lte=1365375284')
				 )
				 .done( function(data){

				 	var why = new app.GridView({ el : $('#content_container'), model : data })

				 })

		    })

		   	app_router.on('route:what', function(){

		    	var what = new app.WhatView({ el : $('#content_container')})

		    })

			app_router.on('route:how', function(){

		    	var how = new app.HowView({ el : $('#content_container') })

		    })

		    app_router.on('route:profile', function(){

		    	var profile = new app.ProfileView({ el : $('#content_container')})

		    })

		    app_router.on('route:addTrackers', function(){

		    	var trackers = new app.AddTrackers( { el : $('#content_container') })

		    })

		    // Start Backbone history a necessary step for bookmarkable URL's
		    Backbone.history.start();

			// var camera, scene, renderer;
			// var controls;

			// var objects = [];
			// var targets = { table: [], sphere: [], helix: [], grid: [] };

			// setTimeout(init, 4000)
			// setTimeout(animate, 4100)

			// function init() {

			// 	camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 1, 5000 );
			// 	camera.position.z = 1800;

			// 	scene = new THREE.Scene();

			// 	var meals = document.getElementsByClassName('meal-container')

			// 	for ( var i = 0; i < meals.length; i ++ ) {

			// 		var element = meals[i]

			// 		element.className = 'element'

			// 		var object = new THREE.CSS3DObject( element );
			// 		object.position.x = Math.random() * 4000 - 2000;
			// 		object.position.y = Math.random() * 4000 - 2000;
			// 		object.position.z = Math.random() * 4000 - 2000;
			// 		scene.add( object );

			// 		objects.push( object );

			// 	}

			// 	var vector = new THREE.Vector3();

			// 	for ( var i = 0, l = objects.length; i < l; i ++ ) {

			// 		var phi = Math.acos( -1 + ( 2 * i ) / l );
			// 		var theta = Math.sqrt( l * Math.PI ) * phi;

			// 		var object = new THREE.Object3D();

			// 		object.position.x = 1000 * Math.cos( theta ) * Math.sin( phi );
			// 		object.position.y = 1000 * Math.sin( theta ) * Math.sin( phi );
			// 		object.position.z = 1000 * Math.cos( phi );

			// 		vector.copy( object.position ).multiplyScalar( 2 );

			// 		object.lookAt( vector );

			// 		targets.sphere.push( object );

			// 	}

			// 	// helix

			// 	var vector = new THREE.Vector3();

			// 	for ( var i = 0, l = objects.length; i < l; i ++ ) {

			// 		var phi = i * 0.175 + Math.PI;

			// 		var object = new THREE.Object3D();

			// 		object.position.x = 1100 * Math.sin( phi );
			// 		object.position.y = - ( i * 8 ) + 450;
			// 		object.position.z = 1100 * Math.cos( phi );

			// 		vector.copy( object.position );
			// 		vector.x *= 2;
			// 		vector.z *= 2;

			// 		object.lookAt( vector );

			// 		targets.helix.push( object );

			// 	}

			// 	// grid

			// 	for ( var i = 0; i < objects.length; i ++ ) {

			// 		var object = new THREE.Object3D();

			// 		object.position.x = ( ( i % 5 ) * 400 ) - 800;
			// 		object.position.y = ( - ( Math.floor( i / 5 ) % 5 ) * 400 ) + 800;
			// 		object.position.z = ( Math.floor( i / 25 ) ) * 1000 - 2000;

			// 		targets.grid.push( object );

			// 	}

			// 	//

			// 	renderer = new THREE.CSS3DRenderer();
			// 	renderer.setSize( window.innerWidth, window.innerHeight );
			// 	renderer.domElement.style.position = 'absolute';
			// 	document.getElementById( 'container' ).appendChild( renderer.domElement );

			// 	//

			// 	controls = new THREE.TrackballControls( camera, renderer.domElement );
			// 	controls.rotateSpeed = 0.5;
			// 	controls.addEventListener( 'change', render );

			// 	var button = document.getElementById( 'table' );
			// 	button.addEventListener( 'click', function ( event ) {

			// 		transform( targets.table, 2000 );

			// 	}, false );

			// 	var button = document.getElementById( 'sphere' );
			// 	button.addEventListener( 'click', function ( event ) {

			// 		transform( targets.sphere, 2000 );

			// 	}, false );

			// 	var button = document.getElementById( 'helix' );
			// 	button.addEventListener( 'click', function ( event ) {

			// 		transform( targets.helix, 2000 );

			// 	}, false );

			// 	var button = document.getElementById( 'grid' );
			// 	button.addEventListener( 'click', function ( event ) {

			// 		transform( targets.grid, 2000 );

			// 	}, false );

			// 	transform( targets.grid, 5000 );

			// 	//

			// 	window.addEventListener( 'resize', onWindowResize, false );

			// }

			// function transform( targets, duration ) {

			// 	TWEEN.removeAll();

			// 	for ( var i = 0; i < objects.length; i ++ ) {

			// 		var object = objects[ i ];
			// 		var target = targets[ i ];

			// 		new TWEEN.Tween( object.position )
			// 			.to( { x: target.position.x, y: target.position.y, z: target.position.z }, Math.random() * duration + duration )
			// 			.easing( TWEEN.Easing.Exponential.InOut )
			// 			.start();

			// 		new TWEEN.Tween( object.rotation )
			// 			.to( { x: target.rotation.x, y: target.rotation.y, z: target.rotation.z }, Math.random() * duration + duration )
			// 			.easing( TWEEN.Easing.Exponential.InOut )
			// 			.start();

			// 	}

			// 	new TWEEN.Tween( this )
			// 		.to( {}, duration * 2 )
			// 		.onUpdate( render )
			// 		.start();

			// }

			// function onWindowResize() {

			// 	camera.aspect = window.innerWidth / window.innerHeight;
			// 	camera.updateProjectionMatrix();

			// 	renderer.setSize( window.innerWidth, window.innerHeight );

			// }

			// function animate() {

			// 	requestAnimationFrame( animate );

			// 	TWEEN.update();
			// 	controls.update();

			// }

			// function render() {

			// 	renderer.render( scene, camera );

			// }

})


Handlebars.registerHelper('ifCond', function(v, options) {
  console.log(v1)
  if(v !== undefine) {
    return options.fn(this);
  }else{
  	options.fn("No Data")
  }
  
});
    

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
					"addTrackers" : "addTrackers",
					"impact" : "impact"
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
					$('#content_container').undelegate('click')

					$.when( 
						$.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000')
					 )
					 .done( function(data){
					 	var why = new app.GridView({ el : $('#content_container'), model : data })
					 })

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
		        
		        $('#content_container').undelegate('click')
		        $('#content_container').show()
				var login = new app.Login({ el : $('#content_container') })

		    })

		    app_router.on('route:nutrition', function() {

		    	$('body').append("<div id='meals_container'></div>")
				var nutrition_view = new app.NutritionView({ el: $('#meals_container') });

		    })

		    app_router.on('route:landingpage', function(){

		    	$('#content_container').undelegate('click')
		    	$('#content_container').show()
		    	var landingpage = new app.LandingPage({ el : $('#content_container')})

		    })

		    app_router.on('route:query', function(){

		    	$('#content_container').undelegate()
		    	$('#content_container').show()
		    	var query = new app.QueryView({ el : $('#content_container')})

		    })

			app_router.on('route:define', function(){

				$('#content_container').undelegate('click')
				$('#content_container').show()
		    	var define = new app.DefineView({ el : $('#content_container')})

		    })

		    app_router.on('route:why', function(){

		    	$('#three').remove()
		    	$('#content_container').undelegate('click')
		    	checkUserStatus()

		    	// var why = new app.GridView({ el : $('#content_container')})
	    		$.when(
					$.getJSON('v1/data/pdarche/body/physicalActivity?created_at__gte=1357020000') //&created_at__lte=1365375284
				 )
				 .done( function(data){

				 	var why = new app.GridView({ el : $('#content_container'), model : data })

				 })

		    })

		   	app_router.on('route:what', function(){

		   		$('#three').remove()
		   		$('#content_container').undelegate('click')
		    	var what = new app.WhatView({ el : $('#content_container')})

		    })

			app_router.on('route:how', function(){

				$('#three').remove()
				$('#content_container').undelegate('click')
		    	var how = new app.HowView({ el : $('#content_container') })

		    })

		    app_router.on('route:impact', function(){
		    	
		    	$('#three').remove()

		    	var container = $('#content_container'),
		    		impact
				
				container.undelegate('click')
				container.empty().hide()
		  //   	impact = new app.ImpactView({ el : container })
				init()

				$.when( $.get('/static/js/templates/impactControls.handlebars'))
				 .done(function(tmpl){
				 	var source = $(tmpl).html(),
				 		template = Handlebars.compile( source )

				 	$('#three').append(template)
				 	
				 	$('#impact_controls_container').mouseover(function(){
						controls.enabled = false
					}).mouseleave(function(){
						controls.enabled = true
					})

					$('#impact_slider').slider({
						slide : function(ev, ui){
							var len = scene.children.length - 1,
								amp = ( ( ui.value ) / 40 ) + 150,
								ppmVal = (( ui.value ) / 200) * 89
								youVal = (ui.value / 2000)

							scene.remove( scene.children[len] )
							addCircle( amp )

							$('#ppm').html(ppmVal)
							console.log("youval", youVal)
							$('#impact_number').html(youVal)
						},
						min : 0,
						max : 4.6 * 2000,
						value : 4.6 * 2000,
					})

				 	$('#comparison_group_drop').change(function(){

					 	addCircle(400)

					 })
				 })

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

var Shaders = {
	'earth' : {
		  uniforms: {
		    'texture': { type: 't', value: THREE.ImageUtils.loadTexture( "/static/img/worldTexture.png" ) }
		  },
		  vertexShader: [
		    'varying vec3 vNormal;',
		    'varying vec2 vUv;',
		    'void main(void) {',
		    'gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
		      'vNormal = normalize( normalMatrix * normal );',
		      'vUv = uv;',
		    '}'
		  ].join('\n'),
		  fragmentShader: [
		    'uniform sampler2D texture;',
		    'varying vec3 vNormal;',
		    'varying vec2 vUv;',
		    'void main(void) {',
		        'vec3 diffuse = texture2D( texture, vUv ).xyz;',
		        'float intensity = 1.05 - dot( vNormal, vec3( 0.0, 0.0, 1.0 ) );',
		        'vec3 atmosphere = vec3( 0.0, 0.0, 0.0 ) * pow( intensity, 3.0 );',
		        'gl_FragColor = vec4(diffuse + atmosphere, 1.0);',
		    '}'
		  ].join('\n')
	}
};

function init(){

	//group to place objects in
	window.partGroup = new THREE.Object3D()
	window.earthGroup = new THREE.Object3D()
	window.group = new THREE.Object3D()

	setupThree()
	addLights()
	addControls()

	// var resolution = 150;
	// var amplitude = 170;
	// var size = 360 / resolution;

	// var geometry = new THREE.Geometry();
	// var material = new THREE.LineBasicMaterial( { color: 0x00FF00, opacity: 1.0} );

	// for(var i = 0; i <= resolution; i++) {
	//     var segment = ( i * size ) * Math.PI / 180;
	//     geometry.vertices.push( 
	//     	new THREE.Vertex( 
	//     		new THREE.Vector3( Math.cos( segment ) * amplitude, 0, Math.sin( segment ) * amplitude ) 
	//     	) 
	//     );
	// }

	addCircle(170)
	addCircle(190)

	// var line = new THREE.Line( geometry, material );
	// scene.add(line);
	
   // background-glow
    planeGeometry = new THREE.PlaneGeometry( 400, 400, 1 );
    planeMaterial = new THREE.MeshBasicMaterial({
		color: 0xFFFFFF,
		map: THREE.ImageUtils.loadTexture("/static/img/bg.png"),
		transparent: true,
		opacity: .6
		// blending: THREE.AdditiveBlending
    });

    plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.position.z = -1000
    plane.scale.x = plane.scale.y = 1.55
    camera.add(plane);

	//earth object	
	window.earthRadius = 120
	var geometry = new THREE.SphereGeometry(earthRadius, 40, 40)
	var shader = Shaders['earth'];
	uniforms = shader.uniforms;

	material = new THREE.ShaderMaterial({
	      uniforms: uniforms,
	      vertexShader: shader.vertexShader,
	      fragmentShader: shader.fragmentShader
	    });

	earth = new THREE.Mesh( geometry, material )
	earth.position.y = -200
	earth.matrixAutoUpdate = false
	earthGroup.add( earth )


	//add everything to scene
	group.add( earthGroup )
	group.add( partGroup )
	scene.add( group )

	setTimeout(loop, 500)


}

function addCircle( distance ){
	
	var resolution = 150;
	var amplitude = distance;
	var size = 360 / resolution;
	var color;

	distance > 170 ? color = 0xFF0000 : color = 0x00FF00

	var geometry = new THREE.Geometry();
	var material = new THREE.LineBasicMaterial( { color: color, opacity: 1.0} );

	for(var i = 0; i <= resolution; i++) {
	    var segment = ( i * size ) * Math.PI / 180;
	    geometry.vertices.push( 
	    	new THREE.Vertex( 
	    		new THREE.Vector3( Math.cos( segment ) * amplitude, 0, Math.sin( segment ) * amplitude ) 
	    	) 
	    );
	}

	var line = new THREE.Line( geometry, material );
	scene.add(line);

}


function loop(){

	group.rotation.y+=.0004

	camera.up = new THREE.Vector3(0, 1, 0)
	camera.lookAt( scene.position );

	render()
	controls.update()

	//  This function will attempt to call loop() at 60 frames per second.
	//  See  this Mozilla developer page for details: https://developer.mozilla.org/en-US/docs/DOM/window.requestAnimationFrame
	window.requestAnimationFrame( loop )
}

function render(){				
	renderer.render( scene, camera )
}

function setupThree(){
	window.scene = new THREE.Scene()

	WIDTH      = $(window).width(),
	HEIGHT     = $(window).height() * .8,
	VIEW_ANGLE = 45,
	ASPECT     = WIDTH / HEIGHT,
	NEAR       = 0.1,
	FAR        = 10000
	
	window.camera = new THREE.PerspectiveCamera( VIEW_ANGLE, ASPECT, NEAR, FAR )
	camera.position.set( 100, 75, 400 ) //starting position of camera - this is desregarded in the loop as its using spherical coordinates
	camera.lookAt( scene.position )
	scene.add( camera )

	window.renderer = new THREE.WebGLRenderer({ antialias: true })
	//window.renderer = new THREE.CanvasRenderer({ antialias: true })
	renderer.setSize( WIDTH, HEIGHT )
	renderer.shadowMapEnabled = true
	renderer.shadowMapSoft = true

	//add canvas to div in DOM
	$('body').prepend('<div id="three"><img src="/static/img/shadow.png" style="position:absolute; top:550px; left:400px;"/></div>')
	$('#three').css({ "position" : "absolute", "top" : "30px", "left" : "0px" })
			   .append( renderer.domElement )

}

function addLights(){
	
	
	window.ambient
	window.directional
	
	
	ambient = new THREE.AmbientLight( 0x666666 )
	group.add( ambient )	
	
	
	// Create a Directional light as pretend sunshine.
	directional = new THREE.DirectionalLight( 0xCCCCCC, .7 )
	directional.castShadow = true
	scene.add( directional )


	directional.position.set( 100, 200, 300 )
	directional.target.position.copy( scene.position )
	directional.shadowCameraTop     =  1000
	directional.shadowCameraRight   =  1000
	directional.shadowCameraBottom  = -1000
	directional.shadowCameraLeft    = -1000
	directional.shadowCameraNear    =  600
	directional.shadowCameraFar     = -600
	directional.shadowBias          =   -0.0001
	directional.shadowDarkness      =    0.4
	directional.shadowMapWidth      = directional.shadowMapHeight = 2048

	// directional.shadowCameraVisible = true
}

function addControls(){

	window.controls = new THREE.TrackballControls( camera )

	controls.rotateSpeed = 1.0
	controls.zoomSpeed   = 1.2
	controls.panSpeed    = 0.8

	controls.noZoom = false
	controls.noPan  = false
	controls.staticMoving = true
	controls.dynamicDampingFactor = 0.3
	controls.keys = [ 65, 83, 68 ]//  ASCII values for A, S, and D

	controls.addEventListener( 'change', render )
}


Handlebars.registerHelper('ifCond', function(v, options) {
  console.log(v1)
  if(v !== undefine) {
    return options.fn(this);
  }else{
  	options.fn("No Data")
  }
  
});
    
var app = app || {};

app.ImpactView = Backbone.View.extend({

    WIDTH : window.innerWidth,
    HEIGHT : window.innerHeight,
    camera : undefined,
    scene : undefined,
    renderer : undefined,
    group : undefined,
    earthRadius : undefined,
    earth : undefined,
    clouds : undefined,
    atmosphere : undefined,
    tilt : 0.41,
    cloudsScale : 1.005,
    mouse2D : undefined, 
    mouse3D : undefined, 
    ray : undefined, 
    theta : 45,
    ROLLOVERED : undefined,
    clock : new THREE.Clock(),
    VIEW_ANGLE : 45,
    ASPECT : this.WIDTH / this.HEIGHT,
    NEAR : 0.1,
    FAR : 10000,

    initialize : function() {

        console.log("here goes nothin.....")

        var self = this
        this.threeInit()
        this.loop() 

        // if ( !($.isFunction(this.template)) ){

        //     $.get('/static/js/templates/impact.handlebars', function(tmpl){
        //         self.template = tmpl
        //         self.render() 
        //     })

        // } else {

        //     console.log("gots the template")

        // }

    },

    render : function() {

        var self = this 

    },

    events : {


    },

    threeInit : function(){

        // add/configure main scene
        this.scene = new THREE.Scene()
        this.camera = new THREE.PerspectiveCamera( this.VIEW_ANGLE, this.ASPECT, this.NEAR, this.FAR )
        this.camera.position.set( 0, 0, 600 )
        this.camera.lookAt( this.scene.position )
        this.scene.add( this.camera )

        // renderer
        this.renderer = new THREE.WebGLRenderer( { clearColor: 0x000000, clearAlpha: 1 } );
        this.renderer.setSize( this.WIDTH, this.HEIGHT );
        this.renderer.sortObjects = false;

        this.renderer.autoClear = false;

        this.$el.append( this.renderer.domElement )

        // create scene
        this.group = new THREE.Object3D()

        var planetTexture = THREE.ImageUtils.loadTexture( "static/img/worldTexture.png" );
        // var cloudsTexture   = THREE.ImageUtils.loadTexture( "static/img/final-images/earth_clouds.png");
        // var normalTexture   = THREE.ImageUtils.loadTexture( "static/media/final-images/earth_normal.jpg" );
        // var specularTexture = THREE.ImageUtils.loadTexture( "static/img/final-images/earth_specular.jpg" );

        //****************** PRIMARY SCENE ELEMENTS ******************

        this.earthRadius = 90
        earth = new THREE.Mesh(
            new THREE.SphereGeometry( this.earthRadius, 64, 64 ),
            new THREE.MeshPhongMaterial( { 
                map: planetTexture,  //THREE.ImageUtils.loadTexture( 'static/media/good-earth/small-map.jpg' ), 
                transparency: true, 
                opacity: 1, 
                ambient: 0xFFFFFF, 
                color: 0xFFFFFF, 
                specular: 0xFFFFFF, 
                shininess: 5, 
                perPixel: true, 
                metal: true 
            })
        )

        earth.position.set( 0, 0, 0 )
        earth.receiveShadow = true
        earth.castShadow = true
        this.group.add( earth )

        //  Check out this really useful resource for understanding the blending modes available in Three.js:
        //  http://mrdoob.github.com/three.js/examples/webgl_materials_blending_custom.html

        // clouds = new THREE.Mesh(
        //     new THREE.SphereGeometry( earthRadius + 2, 32, 32 ),
        //     new THREE.MeshLambertMaterial({ 
        //         color: 0xffffff,
        //         map: cloudsTexture, //THREE.ImageUtils.loadTexture( 'static/media/good-earth/small-clouds.png' ),
        //         transparent: true
        //     })
        // )
        // clouds.position.set( 0, 0, 0 )
        // clouds.receiveShadow = true
        // clouds.castShadow = true
        // group.add( clouds ) 

        this.scene.add( this.group )

        // atmosphere = new THREE.Mesh(
        //     new THREE.SphereGeometry( earthRadius + 4, 32, 32 ),
        //     new THREE.MeshPhongMaterial({
        //         transparency: true, 
        //         opacity: .1, 
        //         ambient: 0xFFFFFF, 
        //         color: 0xFFFFFF, 
        //         specular: 0xFFFFFF, 
        //         shininess: 25, 
        //         perPixel: true
        //     })

        // )
        // atmosphere.position.set( 0, 0, 0 )
        // atmosphere.receiveShadow = true
        // atmosphere.castShadow = true    

        // glowscene.add( atmosphere ) 

        // var renderModel = new THREE.RenderPass( this.scene, this.camera );
        // var effectFilm = new THREE.FilmPass( 0.35, 0.75, 2048, false );

        // effectFilm.renderToScreen = true;

        // this.composer = new THREE.EffectComposer( this.renderer );
        // this.composer.addPass( renderModel );
        // composer.addPass( effectFilm );

        //projector
        // projector = new THREE.Projector();

        // plane = new THREE.Mesh( new THREE.PlaneGeometry( 1000, 1000 ), new THREE.MeshBasicMaterial() );
        // // plane.rotation.x = - Math.PI / 2;
        // plane.rotation.z = - Math.PI / 2;
        // plane.position.z = -50
        // plane.visible = false;
        // scene.add( plane );

        // mouse2D = new THREE.Vector3( 0, 10000, 0.5 );
        // ray = new THREE.Ray( camera.position, null );
        

        //***************** EVENTS ***************** 
        //resize
        window.addEventListener( 'resize', this.onWindowResize, false );

        //mousemove
        // document.addEventListener( 'mousemove', onDocumentMouseMove, false );
    },

    loop : function( self ){

        // this.group.rotation.y  += ( 0.02 ).degreesToRadians()
        // clouds.rotation.y += ( 0.01 ).degreesToRadians()

        // camera.position.z > 300 ? camera.position.z -= 1 : null
        
        //  loop() sSee this Mozilla developer page for details:
        //  https://developer.mozilla.org/en-US/docs/DOM/window.requestAnimationFrame

        requestAnimationFrame( this.loop() )
        this.threeRender()
        // this.controls.update()

    },

    threeRender : function(){

        var delta = this.clock.getDelta();

        this.camera.lookAt( this.scene.position )
        this.renderer.render( this.scene, this.camera )
    
    },

    onWindowResize : function(){

        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize( window.innerWidth, window.innerHeight );

    }

})
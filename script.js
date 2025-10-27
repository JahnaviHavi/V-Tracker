// Get canvas
const canvas = document.getElementById("bg");

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({canvas, alpha: true});
renderer.setSize(window.innerWidth, window.innerHeight);

// Light
const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(10, 10, 10);
scene.add(light);

// Create floating spheres
let spheres = [];
for (let i = 0; i < 7; i++) {
  let geometry = new THREE.SphereGeometry(Math.random() * 2 + 1, 32, 32);
  let material = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.3, roughness: 0.6 });
  let sphere = new THREE.Mesh(geometry, material);

  sphere.position.set(
    (Math.random() - 0.5) * 15,
    (Math.random() - 0.5) * 15,
    (Math.random() - 0.5) * 15
  );

  scene.add(sphere);
  spheres.push(sphere);
}

camera.position.z = 10;

// Animate
function animate() {
  requestAnimationFrame(animate);

  spheres.forEach((s, i) => {
    s.position.x += Math.sin(Date.now() * 0.001 + i) * 0.002;
    s.position.y += Math.cos(Date.now() * 0.001 + i) * 0.002;
  });

  renderer.render(scene, camera);
}

animate();

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

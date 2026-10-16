import type { GLTF } from 'three/addons/loaders/GLTFLoader.js';
import { Mesh, type Material, type Texture } from 'three';

export function disposeGltf(gltf: GLTF): void {
  const textures = new Set<Texture>();
  const materials = new Set<Material>();

  gltf.scene.traverse((object) => {
    if (object instanceof Mesh) {
      object.geometry.dispose();
      const objectMaterials = Array.isArray(object.material)
        ? object.material
        : [object.material];
      for (const material of objectMaterials) {
        materials.add(material);
      }
    }
  });

  for (const material of materials) {
    for (const value of Object.values(material)) {
      if (value && typeof value === 'object' && 'isTexture' in value && value.isTexture) {
        textures.add(value as Texture);
      }
    }
    material.dispose();
  }

  for (const texture of textures) {
    const image = texture.source?.data;
    if (typeof ImageBitmap !== 'undefined' && image instanceof ImageBitmap) {
      image.close();
    }
    texture.dispose();
  }
}

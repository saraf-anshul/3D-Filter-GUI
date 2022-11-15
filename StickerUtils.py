

from random import random
import time


def getIndexFileData(name, version) ->str :
    return f'''Filter: {name}
Version: {version}
Resource: resource.json
PreRequisites:
  - Lib: LibAI
    Assets:
    - Name: facemesh_model_path
      LocalPath: \\"ResourceDir://face_landmark.tflite\\"
    - Name: landmark_metadata_path
      LocalPath: \\"ResourceDir://geometry_pipeline_metadata_landmarks.binarypb\\"
    - Name: facedetection_model_path
      LocalPath: \\"ResourceDir://face_detection_short_range.tflite\\"
  - Lib: LibShutter
    Assets:
    - Name: FaceMesh_3DModel
      LocalPath: \\"ResourceDir://canonical_face_model.obj\\"
    - Name: Occluder_Mat
      LocalPath: \\"ResourceDir://Occluder.mat\\"
    - Name: FACEMASK_MAT
      LocalPath: \\"BaseDir://facemask.mat\\"
    - Name: FACEMASK_TEXTURE
      LocalPath: \\"\\"
Data:
  - Index: 0
    Type: Face3D
    Data:
      - Index: 0
        Type: TextureMask
        Data:
          Texture: FACEMASK_TEXTURE
          FaceID: [0]
          Material: FACEMASK_MAT
          MetalMaterial:
'''

def getShaderData(name : str) -> str:
  return f'''#type vertex
attribute vec3 a_Position;
attribute vec3 a_Normal;
attribute vec2 a_TexCoord;
varying vec2 v_TexCoord;
varying vec3 v_Normal;
uniform mat4 model_mat;
uniform mat4 proj_mat;


vec4 vertex(){{
    v_TexCoord = a_TexCoord;
    v_Normal = a_Normal;
    return proj_mat * model_mat * vec4(a_Position, 1.0);
}}

#type fragment
precision mediump float;
varying vec2 v_TexCoord;
varying vec3 v_Normal;
uniform vec4 u_Color;
uniform vec4 dirlight;

uniform sampler2D u_Albedo;

vec4 fragment(){{
    vec4 texColor = texture2D( u_Albedo, v_TexCoord);
    return vec4(texColor.rgba);
}}

#type shader_data
{{
  \\"ShaderData\\" : [
    {{
      \\"type\\" : \\"Texture2D\\",
      \\"value\\" : \\"{name}\\",
      \\"name\\" : \\"u_Albedo\\",
      \\"function\\" : \\"fragment\\"
    }},
    {{
      \\"type\\" : \\"Vec4\\",
      \\"value\\" : \\"[0.2,0.1,0.3,1.0]\\",
      \\"name\\" : \\"u_Color\\",
      \\"function\\" : \\"fragment\\"
    }}
  ]
}}

#type material_flags_data
{{
  \\"MaterialFlagData\\" : [
    {{
      \\"name\\" : \\"DEPTH_TEST\\",
      \\"type\\" : \\"Boolean\\",
      \\"value\\" : \\"true\\"
    }},
    {{
      \\"name\\" : \\"DEPTH_WRITE\\",
      \\"type\\" : \\"Boolean\\",
      \\"value\\" : \\"true\\"
    }},
    {{
      \\"name\\" : \\"BLEND\\",
      \\"type\\" : \\"Boolean\\",
      \\"value\\" : \\"true\\"
    }},
    {{
      \\"name\\" : \\"BLEND_MODE\\",
      \\"type\\" : \\"INT\\",
      \\"value\\" : \\"2\\"
    }}
  ]
}}

'''

def getResourceFIle():
  return f'''{{
  \\"Assets\\" : 
  [
    {{
      \\"Name\\" : \\"facemesh_model_path\\",
      \\"Url\\"  : \\"\\",
      \\"FallbackUrl\\"  : \\"assets://ai/face_landmark.tflite\\",
      \\"LocalName\\" : \\"face_landmark.tflite\\"
    }},
    {{
      \\"Name\\" : \\"landmark_metadata_path\\",
      \\"Url\\"  : \\"\\",
      \\"FallbackUrl\\"  : \\"assets://ai/geometry_pipeline_metadata_landmarks.binarypb\\",
      \\"LocalName\\" : \\"geometry_pipeline_metadata_landmarks.binarypb\\"
    }},
    {{
      \\"Name\\" : \\"facedetection_model_path\\",
      \\"Url\\"  : \\"\\",
      \\"FallbackUrl\\"  : \\"assets://ai/face_detection_short_range.tflite\\",
      \\"LocalName\\" : \\"face_detection_short_range.tflite\\"
    }},
    {{
      \\"Name\\" : \\"FaceMesh_3DModel\\",
      \\"Url\\"  : \\"\\",
      \\"FallbackUrl\\"  : \\"assets://ai/canonical_face_model.obj\\",
      \\"LocalName\\" : \\"canonical_face_model.obj\\"
    }},
    {{
      \\"Name\\" : \\"Occluder_Mat\\",
      \\"Url\\"  : \\"\\",
      \\"FallbackUrl\\"  : \\"assets://ai/Occluder.mat\\",
      \\"LocalName\\" : \\"Occluder.mat\\"
    }}
  ]
}}
  '''
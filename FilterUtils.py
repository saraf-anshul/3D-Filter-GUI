
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
    - Name: Occluder_Metal_Mat
      LocalPath: \\"ResourceDir://occluder_metal_1671798503.mat\\"
    - Name: FACEMASK_MAT
      LocalPath: \\"BaseDir://facemask.mat\\"
    - Name: FACEMASK_METAL_MAT
      LocalPath: \\"BaseDir://facemask-Metal.mat\\"
    - Name: FACEMASK_TEXTURE
      LocalPath: ""
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
          MetalMaterial: FACEMASK_METAL_MAT
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

def getShaderDataMetal(name : str, flipped : bool) -> str: 
	return f'''#include <metal_stdlib>
#include <metal_matrix>
using namespace metal;

struct VertexGlobalUniformData;
struct FragmentGlobalUniformData;

struct VertexRenderUniformData
{{
    float4x4 u_modelMatrix [[id(0)]];
    float4x4 u_projectionMatrix;
}};

struct FragmentRenderUniformData
{{
    texture2d<float> u_Albedo;
    float4 dirlight;
    float4 u_Color;
}};

struct VertexIn
{{
    float3 a_Position [[attribute(0)]];
    float3 a_Normal [[attribute(1)]];
    float2 a_TexCoord [[attribute(2)]];
}};

struct VertexOut
{{
    float4 position [[position]];
    float2 v_TexCoord;
    float3 v_Normal;
}};

VertexOut vertex vertexShader(constant VertexGlobalUniformData& vertexGlobalUniformData [[buffer(0)]],
                              constant VertexRenderUniformData& vertexRenderUniformData [[buffer(1)]],
                              const VertexIn vertexIn [[stage_in]]) {{
    float3 position = vertexIn.a_Position;
    float2 texCoord = vertexIn.a_TexCoord;
    float3 normal = vertexIn.a_Normal;
    
    VertexOut vertexOut;
    vertexOut.v_TexCoord = texCoord;
    vertexOut.v_Normal = normal;
    vertexOut.position = vertexRenderUniformData.u_projectionMatrix * vertexRenderUniformData.u_modelMatrix * float4(position, 1.0);
    return vertexOut;
}}

float4 fragment fragmentShader(constant FragmentGlobalUniformData& fragmentGlobalUniformData [[buffer(0)]],
                                constant FragmentRenderUniformData& fragmentRenderUniformData [[buffer(1)]],
                                VertexOut vertexOut [[stage_in]]) {{

    float4 texColor = fragmentRenderUniformData.u_Albedo.sample(fragmentGlobalUniformData.u_LinearSampler, vertexOut.v_TexCoord);
    return float4(texColor.rgb, texColor.a * 0.3);
}}

#type shader_data
{{
  \\"ShaderData\\" : [
    {{
      \\"type\\" : \\"Texture2D\\",
      \\"value\\" : \\"{name}\\",
      \\"name\\" : \\"u_Albedo\\",
      \\"scope\\" : \\"RenderUniformData\\",
      \\"isVerticallyFlippedTexture\\": {flipped},
      \\"function\\" : \\"fragment\\"
    }},
    {{
      \\"type\\" : \\"Vec4\\",
      \\"value\\" : \\"[0.2,0.1,0.3,1.0]\\",
      \\"name\\" : \\"u_Color\\",
      \\"scope\\" : \\"RenderUniformData\\",
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

def getResourceMap():
	return {
		"Assets" : 
		[
			{
			"Name" : "facemesh_model_path",
			"Url"  : "https://cdn.sharechat.com/face_landmark.tflite",
			"FallbackUrl"  : "",
			"LocalName" : "face_landmark.tflite"
			},
			{
			"Name" : "landmark_metadata_path",
			"Url"  : "https://cdn.sharechat.com/geometry_pipeline_metadata_landmarks.binarypb",
			"FallbackUrl"  : "",
			"LocalName" : "geometry_pipeline_metadata_landmarks.binarypb"
			},
			{
			"Name" : "facedetection_model_path",
			"Url"  : "https://cdn.sharechat.com/face_detection_short_range.tflite",
			"FallbackUrl"  : "",
			"LocalName" : "face_detection_short_range.tflite"
			},
			{
			"Name" : "FaceMesh_3DModel",
			"Url"  : "https://cdn.sharechat.com/canonical_face_model.obj",
			"FallbackUrl"  : "",
			"LocalName" : "canonical_face_model.obj"
			},
			{
			"Name" : "Occluder_Mat",
			"Url"  : "https://cdn.sharechat.com/Occluder.mat",
			"FallbackUrl"  : "",
			"LocalName" : "Occluder.mat"
			},
      {
      "Name": "Occluder_Metal_Mat",
      "Url": "https://cdn.sharechat.com/occluder_metal_1671798503.mat",
      "FallbackUrl": "",
      "LocalName": "occluder_metal_1671798503.mat"
      }
		]
	}


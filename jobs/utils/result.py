def replace_tabs_with_spaces(input_string):
    # Sử dụng phương thức replace để thay thế '\t' bằng ' '
    modified_string = input_string.replace('\t', ' ')
    return modified_string

# Ví dụ sử dụng hàm replace_tabs_with_spaces
input_string = "ecomerceshop\tweb\t2024-04-18 13:52:55.907\t2024-04-18 13:52:50.638\t2024-04-18 13:52:50.251\tunstruct\t9f020764-ef04-4b15-aa9a-b8a68a328e0d\t\ttracking_product\tjs-3.22.0\tssc-3.1.0-kafkasink\tsnowplow-enrich-kafka-3.8.0\t\t172.18.0.1\t\t56445e4a-4a5f-42c3-9106-41a9dda41df3\t35\tacdddabe-d922-4e28-b6bc-af74351abe04\t\t\t\t\t\t\t\t\t\t\t\thttp://localhost:5173/productDescription/16\t\t\thttp\tlocalhost\t5173\t/productDescription/16\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{\"schema\":\"iglu:com.snowplowanalytics.snowplow/contexts/jsonschema/1-0-1\",\"data\":[{\"schema\":\"iglu:nana.shop/product_entity/jsonschema/1-0-0\",\"data\":{\"name\":\"Ch\u00e2n V\u00e1y Jean N\u1eef D\u00e0i Ch\u1eef A T\u00fai \u0110\u1eafp Tr\u01a1n Form A Line\",\"price\":54000,\"id\":\"16\",\"category\":\"Accessories\"}},{\"schema\":\"iglu:com.snowplowanalytics.snowplow/web_page/jsonschema/1-0-0\",\"data\":{\"id\":\"5a5cd806-fcc4-4d97-8bc6-2ab1c70b972e\"}}]}\t\t\t\t\t\t{\"schema\":\"iglu:com.snowplowanalytics.snowplow/unstruct_event/jsonschema/1-0-0\",\"data\":{\"schema\":\"iglu:nana.shop/product_action/jsonschema/1-0-0\",\"data\":{\"action\":\"view\"}}}\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0\t\t\t\t\t\ten-US\t\t\t\t\t\t\t\t\t\t1\t24\t1872\t924\t\t\t\t\t\t\t1920\t1080\tUTF-8\t1864\t1039\t\t\t\t\t\t\t\t\t\t\t\t2024-04-18 13:52:50.255\t\t\t{\"schema\":\"iglu:com.snowplowanalytics.snowplow/contexts/jsonschema/1-0-1\",\"data\":[{\"schema\":\"iglu:nl.basjes/yauaa_context/jsonschema/1-0-4\",\"data\":{\"deviceBrand\":\"Unknown\",\"deviceName\":\"Desktop\",\"operatingSystemVersionMajor\":\">=10\",\"layoutEngineNameVersion\":\"Blink 123\",\"operatingSystemNameVersion\":\"Windows >=10\",\"agentInformationEmail\":\"Unknown\",\"networkType\":\"Unknown\",\"webviewAppNameVersionMajor\":\"Unknown ??\",\"layoutEngineNameVersionMajor\":\"Blink 123\",\"operatingSystemName\":\"Windows NT\",\"agentVersionMajor\":\"123\",\"layoutEngineVersionMajor\":\"123\",\"webviewAppName\":\"Unknown\",\"deviceClass\":\"Desktop\",\"agentNameVersionMajor\":\"Edge 123\",\"operatingSystemNameVersionMajor\":\"Windows >=10\",\"deviceCpuBits\":\"64\",\"webviewAppVersionMajor\":\"??\",\"operatingSystemClass\":\"Desktop\",\"webviewAppVersion\":\"??\",\"layoutEngineName\":\"Blink\",\"agentName\":\"Edge\",\"agentVersion\":\"123\",\"layoutEngineClass\":\"Browser\",\"agentNameVersion\":\"Edge 123\",\"operatingSystemVersion\":\">=10\",\"deviceCpu\":\"Intel x86_64\",\"agentClass\":\"Browser\",\"layoutEngineVersion\":\"123\",\"agentInformationUrl\":\"Unknown\"}}]}\t9cc0b453-f1ae-42a7-9c34-4a212e35be41\t2024-04-18 13:52:50.634\tnana.shop\tproduct_action\tjsonschema\t1-0-0\t\t"
result_string = replace_tabs_with_spaces(input_string)
print("Chuỗi sau khi xử lý:", result_string)
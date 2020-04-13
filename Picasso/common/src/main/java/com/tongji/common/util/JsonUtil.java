package com.tongji.common.util;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionLikeType;
import com.fasterxml.jackson.databind.type.TypeFactory;
import com.tongji.common.enums.APICodeEnum;
import com.tongji.common.exception.AppInternalError;
import org.springframework.util.StringUtils;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class JsonUtil {
    private final static ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    private static TypeFactory factory = OBJECT_MAPPER.getTypeFactory();

    public static ObjectMapper getObjectMapper() {
        return OBJECT_MAPPER;
    }

    public static <T> T jsonToObject(String json, Class<T> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> T jsonToObject(String json, Class<T> valueType, T defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> T jsonToObject(String json, JavaType valueType) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> T jsonToObject(String json, JavaType valueType, T defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> T jsonToObject(String json, TypeReference<T> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> T jsonToObject(String json, TypeReference<T> valueType, T defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> T jsonToObject(String json, CollectionLikeType valueType) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> T jsonToObject(String json, CollectionLikeType valueType, T defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T, P> T jsonToTemplateObject(String json, Class<T> parametrizedClass, Class<P> parameterClass) {
        JavaType javaType = OBJECT_MAPPER.getTypeFactory().constructParametricType(parametrizedClass, parameterClass);

        try {
            return OBJECT_MAPPER.readValue(json, javaType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T, P> T jsonToTemplateObject(String json, Class<T> parametrizedClass, Class<P> parameterClass, T defaultValue) {
        JavaType javaType = OBJECT_MAPPER.getTypeFactory().constructParametricType(parametrizedClass, parameterClass);

        try {
            return OBJECT_MAPPER.readValue(json, javaType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> List<T> jsonToList(String json, Class<T> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructCollectionType(List.class, valueType));
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> List<T> jsonToList(String json, Class<T> valueType, List<T> defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructCollectionType(List.class, valueType));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> Set<T> jsonToSet(String json, Class<T> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructCollectionType(Set.class, valueType));
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> Set<T> jsonToSet(String json, Class<T> valueType, Set<T> defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructCollectionType(Set.class, valueType));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <T> Map<String, T> jsonToMap(String json, Class<T> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructMapType(Map.class, String.class, valueType));
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <T> Map<String, T> jsonToMap(String json, Class<T> valueType, Map<String, T> defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructMapType(Map.class, String.class, valueType));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <K, V> Map<K, V> jsonToMap(String json, TypeReference<Map<K, V>> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <K, V> Map<K, V> jsonToMap(String json, TypeReference<Map<K, V>> valueType, Map<K, V> defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json, valueType);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static <K, V> Map<K, V> jsonToMap(String json, Class<K> keyType, Class<V> valueType) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructMapType(Map.class, keyType, valueType));
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static <K, V> Map<K, V> jsonToMap(String json, Class<K> keyType, Class<V> valueType, Map<K, V> defaultValue) {
        try {
            return OBJECT_MAPPER.readValue(json,
                    factory.constructMapType(Map.class, keyType, valueType));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    public static String objectToJson(Object value) {
        try {
            return OBJECT_MAPPER.writeValueAsString(value);
        } catch (JsonProcessingException e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", value));
        }
    }

    public static String objectToJson(Object value, String defaultValue) {
        try {
            return OBJECT_MAPPER.writeValueAsString(value);
        } catch (JsonProcessingException e) {
            return defaultValue;
        }
    }

    public static JsonNode objectToJsonNode(Object value) {
        return OBJECT_MAPPER.valueToTree(value);
    }

    public static JsonNode jsonToJsonNode(String json) {
        try {
            return OBJECT_MAPPER.readTree(json);
        } catch (Exception e) {
            throw new AppInternalError(String.format(APICodeEnum.INTERN_ERROR + "%s", json));
        }
    }

    public static JsonNode jsonToJsonNode(String json, JsonNode defaultJsonNode) {
        try {
            return OBJECT_MAPPER.readTree(json);
        } catch (Exception e) {
            return defaultJsonNode;
        }
    }

    /**
     * @deprecated Use {@link #jsonToMap(String, Class)} instead
     */
    @Deprecated
    public static Map<String, Object> decodeJsonToMap(String json) {
        if (StringUtils.isEmpty(json)) {
            return null;
        }
        try {
            return OBJECT_MAPPER.readValue(json, Map.class);
        } catch (JsonParseException e) {
        } catch (JsonMappingException e) {
        } catch (IOException e) {
        }
        return null;
    }

    /**
     * @deprecated Use {@link #jsonToList(String, Class)} instead
     */
    @Deprecated
    @SuppressWarnings("unchecked")
    public static List<Object> decodeJsonToList(String json) {
        try {
            return OBJECT_MAPPER.readValue(json, List.class);
        } catch (JsonParseException e) {
        } catch (JsonMappingException e) {
        } catch (IOException e) {
        }
        return null;
    }

    /**
     * @deprecated Use {@link #jsonToObject(String, Class, Object)} instead
     */
    @Deprecated
    public static <T> T decodeJson(String json, Class<T> type) {
        return jsonToObject(json, type, null);
    }

    /**
     * @deprecated Use {@link #objectToJson(Object, String)} (String, Class)} instead
     */
    @Deprecated
    public static String jsonEncode(Object obj) {
        return objectToJson(obj, null);
    }
}

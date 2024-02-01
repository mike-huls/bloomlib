use bincode;
use serde::Serialize;
pub fn serialize<T: Serialize>(value: &T) -> Vec<u8> {
    serde_json::to_vec(value).expect("Failed to serialize value")
    // bincode::serialize(value).expect("Failed to serialize value")
}

//! Python bindings for the Rust BloomFilter

use pyo3::prelude::{pyclass, pymethods, pymodule, PyModule};
use pyo3::{PyObject, PyResult, Python};
use pyo3::types::{
    PyString, PyInt, PyFloat, PyDate, PyDateTime, PyDict, PyList, PyTuple, PySet, PyTime,
    PyBool, PyLong, PyFunction
};
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use pyo3::prelude::*;
use crate::bloom_filter::BloomFilterRS;  // For Python, PyResult

mod bloom_filter;
mod serialization;
mod counting_bloom_filter;


// Standard Bloom Filter
#[pyclass]
struct BloomFilter {
    bloomfilter: BloomFilterRS
}

#[pymethods]
impl BloomFilter {
    #[new]
    pub fn new(expected_number_of_items: usize, desired_false_positive_rate: f64) -> Self {
        BloomFilter {
            bloomfilter: BloomFilterRS::new(expected_number_of_items, desired_false_positive_rate),
        }
    }

    pub fn add(&mut self, py: Python, item: PyObject) -> PyResult<()> {

        // Create a mutable Vec<u8> to store the hash bytes
        let mut py_bytes: Vec<u8> = Vec::new();

        // Populate the hash bytes vector
        hash_pyobject(py, &item, &mut py_bytes)?;

        // Use the hash bytes to update the BloomSet
        self.bloomfilter.add_bytes(&py_bytes);

        Ok(())
    }

    pub fn add_bulk(&mut self, py: Python, items: &PyAny) -> PyResult<()> {
    // Check if the provided argument is an iterator
    if let Ok(item_iterator) = items.iter() {
        // Iterate over each item
        for item in item_iterator {
            self.add(py, item?.extract()?)?;
        }
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "Expected an iterable",
        ));
    }
    Ok(())
}

    pub fn contains(&self, py: Python, item: PyObject) -> PyResult<bool> {

        // Create a mutable Vec<u8> to store the hash bytes
        let mut py_bytes: Vec<u8> = Vec::new();

        // Populate the hash bytes vector
        hash_pyobject(py, &item, &mut py_bytes)?;

        // use Python built-in hash function if we cannot hash the object efficiently
        if py_bytes.is_empty() {
            let hash_val: i64 = item.call_method0(py, "__hash__")?.extract(py)?;
            // Convert the i64 hash value to bytes and extend py_bytes
            py_bytes.extend_from_slice(&hash_val.to_ne_bytes());
        }

        // Return boolean
        Ok(self.bloomfilter.contains_bytes(&py_bytes))
    }
    pub fn clear(&mut self) -> PyResult<()> {
        self.bloomfilter.clear();
        Ok(())
    }
    pub fn get_number_of_hashes(&self, py: Python) -> PyResult<Py<PyLong>> {
        let py_hash_count: PyObject = self.bloomfilter.get_hash_count().into_py(py);
        let py_long_hash_count = py_hash_count.extract::<Py<PyLong>>(py)?;
        Ok(py_long_hash_count)
    }
    pub fn get_number_of_bits(&self, py: Python) -> PyResult<Py<PyLong>> {
        let bitlen: PyObject = self.bloomfilter.get_bit_count().into_py(py);
        let py_long_biglen = bitlen.extract::<Py<PyLong>>(py)?;
        Ok(py_long_biglen)
    }
    pub fn estimate_false_positive_rate(&self) -> f64 {
        self.bloomfilter.estimate_false_positive_rate()
    }
}




/// Hashes Python Objects. Returns Bytes
fn hash_pyobject(py: Python, obj: &PyObject, output: &mut Vec<u8>) -> PyResult<()> {
    let mut hasher = DefaultHasher::new();

    let py_any = obj.as_ref(py);

    match py_any {
        // Combine integer types
        obj if obj.cast_as::<PyInt>().is_ok() || obj.cast_as::<PyLong>().is_ok() => {
            obj.extract::<i64>()?.hash(&mut hasher)
        },

        // Floats
        obj if obj.cast_as::<PyFloat>().is_ok() => {
            obj.extract::<f64>()?.to_bits().hash(&mut hasher)
        },

        // Booleans
        obj if obj.cast_as::<PyBool>().is_ok() => {
            obj.extract::<bool>()?.hash(&mut hasher)
        },

        // Combine string and various collections into one case
        obj if obj.cast_as::<PyString>().is_ok()
            || obj.cast_as::<PyList>().is_ok()
            || obj.cast_as::<PyDict>().is_ok()
            || obj.cast_as::<PyTuple>().is_ok()
            || obj.cast_as::<PySet>().is_ok() => {
            obj.str()?.to_string().hash(&mut hasher)
        },

        // Date and time types
        obj if obj.cast_as::<PyDate>().is_ok()
            || obj.cast_as::<PyDateTime>().is_ok()
            || obj.cast_as::<PyTime>().is_ok() => {
            obj.call_method0("isoformat")?.to_string().hash(&mut hasher)
        },

        // Functions get converted to string and hashed
        obj if obj.cast_as::<PyFunction>().is_ok() => {
            obj.str()?.to_string().hash(&mut hasher)
        },

        obj if obj.cast_as::<PyDict>().is_ok() => {
            let dict: &PyDict = obj.extract()?;
            for (key, value) in dict.into_iter() {
                key.to_string().hash(&mut hasher);
                hash_pyobject(py, &value.to_object(py), output)?;
            }
        },

        // Default case for other types
        _ => {
            // Call Python's `__hash__` function to get a hash value todo this should be optimized
            let hash_val: i64 = obj.call_method0(py, "__hash__")?.extract(py)?;
            hasher.write_i64(hash_val);
        },
    };

    let hash_bytes = hasher.finish().to_ne_bytes();
    output.extend_from_slice(&hash_bytes);

    Ok(())

}


/// Create the Python module
#[pymodule]
fn bloomlib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<BloomFilter>()?;
//     m.add_function(wrap_pyfunction!(estimate_false_positive_rate, m)?)?;
    Ok(())
}




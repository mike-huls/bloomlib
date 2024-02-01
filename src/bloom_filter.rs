//! BloomFilter implementation in Rust

use std::io::Cursor;

use serde::{Serialize, Deserialize};
use std::f64::consts::LN_2;
use std::hash::{Hash};
use murmur3;
use crate::serialization;

///
///- m     number of bits
///- n     estimated number of elements (to be) inserted
///- p     desired false positive rate
///- k     number of hash functions
///

/// Calculates optimal number of bits to use for the bloom filter
/// This is calculated by `m = -(n * ln(p)) / ln(2)^2)`
///     - m     optimal number of bits          (integer)
///     - n     (estimated) number of items     (integer)
///     - p     desired false positive rate     (float 0..1)
///
/// # Arguments
/// * `expected_number_of_items` - Estimated number of items that the BloomFilter should accommodate
/// * `desired_false_pos_rate` - Desired/accepted false positive rate
///
/// # Examples
/// ```
/// // You can have rust code between fences inside the comments
/// // If you pass --test to `rustdoc`, it will even test it for you!
/// // use doc::Person;
/// //let person = Person::new("name");
/// ```
pub fn calc_optimal_number_of_bits(expected_number_of_items: usize, desired_false_pos_rate:f64) -> usize {
    let num = -1.0_f64 * expected_number_of_items as f64 * desired_false_pos_rate.ln();
    let denominator = 2.0_f64.ln().powf(2.0);
    (num / denominator).ceil() as usize
}


/// Calculates optimal number of hashes for the bloom filter
/// This is calculated by `k = (m / n ) * ln2`
///     - m     optimal number of bits          (integer)
///     - n     (estimated) number of items     (integer)
///     - p     desired false positive rate     (float 0..1)
///
/// # Arguments
/// * `expected_number_of_items` - Estimated number of items that the BloomFilter should accomodate
/// * `bit_array_size` - Number of bits reserved for the BloomFilter
///
/// # Examples
/// ```
/// // You can have rust code between fences inside the comments
/// // If you pass --test to `rustdoc`, it will even test it for you!
/// use doc::Person;
/// let person = Person::new("name");
/// ```
pub fn calculate_optimal_number_of_hashes(bit_array_size:usize, expected_number_of_items:usize ) -> usize {
    ((bit_array_size as f64 / expected_number_of_items as f64) * LN_2).ceil() as usize
}



/// A struct representing a BloomFilter
#[derive(Serialize, Deserialize)]
pub struct BloomFilterRS {
    /// Memory size; number of bits
    pub bitvec: Vec<u8>,    // todo rename to vector_of_bytes? upgrade to array if possible?
    /// The number of time an item should be hashed with different types of hash functions or seeds
    pub hashes: usize,      // todo rename to hash_functions (isnt this always a small, positive integer?)
    /// The expected number of items this Bloom Filter should hold
    expected_n_items:usize,
}

impl BloomFilterRS {
    pub fn new(expected_number_of_items: usize, desired_false_positive_rate: f64) -> Self {
        // todo fp_rate to f64 or smaller?
        let num_of_bits = calc_optimal_number_of_bits(expected_number_of_items, desired_false_positive_rate);
        let num_of_hashes = calculate_optimal_number_of_hashes(num_of_bits, expected_number_of_items);

        BloomFilterRS {
            bitvec: vec![0; num_of_bits / 8],
            hashes: num_of_hashes,
            expected_n_items: expected_number_of_items
        }
    }

    pub fn add_bytes(&mut self, hash_bytes: &[u8]) {
        for i in 0..self.hashes {
            // let hash_value = fasthash::murmur3::hash32_with_seed(hash_bytes, i as u32);
            let mut reader = Cursor::new(hash_bytes);
            let hash_value = murmur3::murmur3_32(&mut reader, i as u32).unwrap();

            let index = hash_value % (self.bitvec.len() as u32 * 8);  // Total number of bits
            // println!("a idx: {:?}", &index);

            let byte_pos = (index / 8) as usize;  // Position of the byte in the vector
            let bit_pos = index % 8;             // Position of the bit in the byte
            self.bitvec[byte_pos] |= 1 << bit_pos;      // set bit at pos to 1 if it isnt already
        }
    }


    /// Adds an item to the BloomFilter
    pub fn add<T: Serialize + Hash>(&mut self, item: &T) {
        let serialized_item = serialization::serialize(item);
        self.add_bytes(&serialized_item);
    }

    /// Checks if a given item may be contained by the BloomFilter
    /// True: maybe
    /// False: definitely no
    pub fn contains_bytes(&self, hash_bytes: &[u8]) -> bool {
        for i in 0..self.hashes {
            let mut reader = Cursor::new(hash_bytes);
            let hash_value = murmur3::murmur3_32(&mut reader, i as u32).unwrap();

            let index = hash_value % (self.bitvec.len() as u32 * 8);
            // println!("c idx: {:?}", &index);
            let byte_pos = (index / 8) as usize;
            let bit_pos = index % 8;

            // If any bit is not set, the item is definitely not in the filter
            if self.bitvec[byte_pos] & (1 << bit_pos) == 0 {
                return false;
            }
        }

        // If all bits are set, the item might be in the filter
        return true;

    }
    /// Check is a biven item may be contained in the BLoomFilter
    pub fn contains<T: Serialize>(&self, item: &T) -> bool {
        let serialized_item = serialization::serialize(item);
        // println!("c val: {:?}", &serialized_item);

        return self.contains_bytes(&serialized_item);
    }

    /// Clears the current BLoom filter
    pub fn clear(& mut self) {
        let filter_len = self.bitvec.len();
        self.bitvec = vec![0; filter_len];
    }

    /// Estimates the false positive rate.
    ///
    /// # Arguments
    ///
    /// * `n_hashes` - The number of hash functions used.
    /// * `n_bits` - The number of bits in the filter.
    /// * `expected_n_of_items` - The expected number of items to be inserted.
    ///
    /// # Example
    /// ```
    /// let rate = estimate_false_positive_rate(3, 1000, 300);
    /// ```
    pub fn estimate_false_positive_rate(&self) -> f64 {
        let n_hashes_f64 = self.hashes as f64;
        let n_bits_f64 = self.bitvec.len() as f64;
        let expected_n_of_items_f64 = self.expected_n_items as f64;

        (1.0 - f64::exp(-n_hashes_f64 * expected_n_of_items_f64 / n_bits_f64)).powf(n_hashes_f64)
    }
}


#[cfg(test)]
mod tests_insert_and_get {
    use super::*;
    use serde::{Serialize, Deserialize};
    use crate::bloomlib;

    #[derive(Serialize, Deserialize, Hash)]
    struct TestItem {
        key: i32,
        value: String,
    }

    #[test]
    fn test_add_and_contains() {
        let mut bf = BloomFilterRS::new(10, 0.01);

        bf.add(&"test");
        bf.add(&1);


        println!("bitsize: {}", bf.bitvec.len());
        println!("n hashes: {}", bf.hashes);

        // println!("not bar: {}", bf.contains(&"bar"));
        // println!("yes test: {}", bf.contains(&"test"));
        // println!("not 1: {}", bf.contains(&1));

        // Uncomment and fix these assertions
        assert!(bf.contains(&"test"), "Item 'test' should be in the BloomFilter");
        assert!(bf.contains(&1), "Item 'test' should be in the BloomFilter");
        // not in
        assert!(!bf.contains(&"bar"), "Item 'bar' should not be in the BloomFilter");
        assert!(!bf.contains(&"nee"), "Item 'nee' should not be in the BloomFilter");

    }

    #[test]
    fn test_add_and_get_objects() {
        let mut bloom_filter = BloomFilterRS::new(100, 0.01);
        let item = TestItem { key: 1, value: "test".to_string() };

        // Item should not be in the filter initially
        assert!(!bloom_filter.contains(&item), "Item should not be in the filter yet");

        bloom_filter.add(&item);

        // Item should be in the filter after adding
        assert!(bloom_filter.contains(&item), "Item should be in the filter after adding");
        assert!(!bloom_filter.contains(&"hello"), "Item should be in the filter after adding");
    }
    #[test]
    fn test_add_multiple_items() {
        let mut bf = BloomFilterRS::new(3, 0.01);

        bf.add(&"een");
        bf.add(&"twee");
        bf.add(&"drie");


        println!("bitsize: {}", bf.bitvec.len());
        println!("n hashes: {}", bf.hashes);

        // Uncomment and fix these assertions
        assert!(bf.contains(&"een"), "Item 'een' should be in the BloomFilter");
        assert!(bf.contains(&"twee"), "twee 'twee' should be in the BloomFilter");
        // not in
        assert!(!bf.contains(&"nope"), "Item 'nope' should not be in the BloomFilter");
        assert!(!bf.contains(&"nein"), "Item 'nein' should not be in the BloomFilter");

    }

    #[test]
    fn test_insert_and_contains() {
        let mut bf = BloomFilterRS::new(3, 0.01);

        bf.add(&"test");
        bf.add(&1);


        println!("bitsize: {}", bf.bitvec.len());
        println!("n hashes: {}", bf.hashes);

        // Uncomment and fix these assertions
        assert!(bf.contains(&"test"), "Item 'test' should be in the BloomFilter");
        assert!(bf.contains(&1), "Item 'test' should be in the BloomFilter");
        // not in
        assert!(!bf.contains(&"bar"), "Item 'bar' should not be in the BloomFilter");
        assert!(!bf.contains(&"nee"), "Item 'nee' should not be in the BloomFilter");

    }

    #[test]
    fn test_clear_filter() {
        let mut bloom_filter = BloomFilterRS::new(100, 0.01);
        let item = TestItem { key: 1, value: "test".to_string() };
        assert!(!bloom_filter.contains(&item), "Item should not be in the filter yet");
        bloom_filter.add(&item);
        assert!(bloom_filter.contains(&item), "Item should be in the filter after adding");
        bloom_filter.clear();
        assert!(!bloom_filter.contains(&item), "Item shouldnt be in filter since it's cleared");

    }
    #[test]
    fn test_add_and_get_bytes_directly() {
        let mut bloom_filter = BloomFilterRS::new(100, 0.01);

        // Generate a random byte array
        let some_bytes: Vec<u8> = vec![12, 48, 94, 127, 255];

        // Ensure the bytes are not in the filter initially
        assert!(!bloom_filter.contains_bytes(&some_bytes), "Bytes should not be in the filter yet");

        bloom_filter.add_bytes(&some_bytes);

        // Now the bytes should be in the filter
        assert!(bloom_filter.contains_bytes(&some_bytes), "Bytes should be in the filter after adding");
    }

    #[test]
    fn test_serialization() {
        let mut bloom_filter = BloomFilterRS::new(100, 0.01);
        bloom_filter.add(&"test item");

        let serialized = serde_json::to_string(&bloom_filter).expect("Failed to serialize");
        // println!("serialized: {}", serialized);
        let deserialized: BloomFilterRS = serde_json::from_str(&serialized).expect("Failed to deserialize");

        assert!(deserialized.contains(&"test item"), "Deserialized filter should contain the item");
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde::{Serialize, Deserialize};

    #[derive(Serialize, Deserialize, Hash)]
    struct TestItem {
        key: i32,
        value: String,
    }



    #[test]
    fn test_false_positive_rate() {
        let n = 500_000; // Number of items to insert
        let p = 0.05; // Desired false positive probability
        let mut bloom_filter = BloomFilterRS::new(n, p);

        println!("hashes: {}", bloom_filter.hashes);
        println!("bits: {}", bloom_filter.bitvec.len());


        // Insert `n` items into the filter
        for i in 0..n {
            bloom_filter.add(&i);
        }

        // Check `n` different items and count the false positives
        let fp_count_observed = (n..n*2).filter(|&i| {
            // println!("does {} contain? {}", &i, bloom_filter.contains(&i));
            bloom_filter.contains(&i)
        }).count();

        println!("contains n+1: {}", bloom_filter.contains(&10001));
        println!("contains n*2: {}", bloom_filter.contains(&20000));
        println!("contains n - 1: {}", bloom_filter.contains(&9999));


        let fp_count_expected = (n as f64 * p) as usize;
        println!("bitlen: {}", bloom_filter.bitvec.len());
        println!("hashes: {}", bloom_filter.hashes);
        println!("fp's expected: {}", fp_count_expected);
        println!("fp's observed: {}", fp_count_observed);
        println!("fp-rate estimate: {}", bloom_filter.estimate_false_positive_rate());
        assert!(
            fp_count_observed <= fp_count_expected,
            "Too many false positives: {}, expected at most {}", fp_count_observed, fp_count_expected
        );
    }

    #[test]
    fn test_can_estimate_false_positive_rate() {
        let n = 1000; // Number of items to insert
        let p = 0.01; // Desired false positive probability
        let mut bloom_filter = BloomFilterRS::new(n, p);

        println!("test: {}", bloom_filter.estimate_false_positive_rate());

        assert!(bloom_filter.estimate_false_positive_rate() != 0.0, "Estimated false positive rate cannot be 0");
    }

    #[test]
    fn test_false_positive_rate_cgpt() {
        // Setup
        let n = 10000; // Number of items to insert
        let p = 0.01; // Desired false positive probability
        let mut bloom_filter = BloomFilterRS::new(n, p);

        // Insert `n` items into the filter
        for i in 0..n {
            let item = format!("item{}", i);
            bloom_filter.add(&item);
        }

        // Check `n` different items and count the false positives
        let fp_count_observed = (n..2*n).filter(|&i| {
            let item = format!("item{}", i); // Assuming bloom_filter.contains expects a &str
            bloom_filter.contains(&item)
        }).count();

        // Calculate the expected number of false positives
        let fp_count_expected = (n as f64 * p).round() as usize;

        println!("Expected false positives: {}", fp_count_expected);
        println!("Observed false positives: {}", fp_count_observed);

        // Assert that the observed false positives do not exceed the expected amount
        assert!(
            fp_count_observed <= fp_count_expected,
            "Observed more false positives than expected: {}, expected at most {}", fp_count_observed, fp_count_expected
        );
    }


}
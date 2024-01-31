use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

struct CountingBloomFilter {
    filter: Vec<u32>,
    size: usize,
    hash_functions: u32,
}

impl CountingBloomFilter {
    fn new(size: usize, hash_functions: u32) -> Self {
        CountingBloomFilter {
            filter: vec![0; size],
            size,
            hash_functions,
        }
    }

    fn add<T: Hash>(&mut self, item: &T) {
        for i in 0..self.hash_functions {
            let index = self.get_index(item, i);
            self.filter[index] += 1;
        }
    }

    fn contains<T: Hash>(&self, item: &T) -> bool {
        for i in 0..self.hash_functions {
            let index = self.get_index(item, i);
            if self.filter[index] == 0 {
                return false;
            }
        }
        true
    }

    fn remove<T: Hash>(&mut self, item: &T) {
        for i in 0..self.hash_functions {
            let index = self.get_index(item, i);
            if self.filter[index] > 0 {
                self.filter[index] -= 1;
            }
        }
    }

    fn get_index<T: Hash>(&self, item: &T, i: u32) -> usize {
        let mut hasher = DefaultHasher::new();
        item.hash(&mut hasher);
        let hash = hasher.finish();
        ((hash.wrapping_add(i as u64).wrapping_add(i.pow(2) as u64)) as usize) % self.size
    }
}

fn main() {
    let mut bloom_filter = CountingBloomFilter::new(100, 3);

    bloom_filter.add(&"item1");
    println!("Contains item1? {}", bloom_filter.contains(&"item1"));

    bloom_filter.remove(&"item1");
    println!("Contains item1 after removal? {}", bloom_filter.contains(&"item1"));
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_check() {
        let mut bloom_filter = CountingBloomFilter::new(100, 3);
        assert_eq!(bloom_filter.contains(&"item1"), false);
        bloom_filter.add(&"item1");
        assert_eq!(bloom_filter.contains(&"item1"), true);
    }

    #[test]
    fn test_remove() {
        let mut bloom_filter = CountingBloomFilter::new(100, 3);
        bloom_filter.add(&"item1");
        assert_eq!(bloom_filter.contains(&"item1"), true);
        bloom_filter.remove(&"item1");
        assert_eq!(bloom_filter.contains(&"item1"), false);
    }

    #[test]
    fn test_false_positive() {
        let mut bloom_filter = CountingBloomFilter::new(100, 3);
        bloom_filter.add(&"item1");
        // Note: This test may fail due to the probabilistic nature of Bloom filters
        assert_eq!(bloom_filter.contains(&"item2"), false);
    }

    #[test]
    fn test_multiple_items() {
        let mut bloom_filter = CountingBloomFilter::new(100, 3);
        bloom_filter.add(&"item1");
        bloom_filter.add(&"item2");
        assert_eq!(bloom_filter.contains(&"item1"), true);
        assert_eq!(bloom_filter.contains(&"item2"), true);
        bloom_filter.remove(&"item1");
        assert_eq!(bloom_filter.contains(&"item1"), false);
        assert_eq!(bloom_filter.contains(&"item2"), true);
    }
}

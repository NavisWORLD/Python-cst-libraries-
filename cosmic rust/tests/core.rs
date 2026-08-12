use std::fs;
use std::sync::{Arc, Mutex};

use cosmic_rust::{
    check_preflight, Dyn12, Event, EventBus, GaussianSynapse, HebbianMemory, Lorenz, SemanticMemory,
};

#[test]
fn dyn12_persists_state() {
    let mut dyn12 = Dyn12::new();
    dyn12.0.update(&[1.0], 1.0).unwrap();
    dyn12.0.update(&[0.0], 1.0).unwrap();
    assert_eq!(dyn12.0.dimension(), 12);
    assert_eq!(dyn12.0.updates(), 2);
    assert!(dyn12.0.l2() > 0.0);
}

#[test]
fn gaussian_synapse_is_live() {
    let states = vec![vec![0.0, 0.0], vec![1.0, 0.5], vec![0.2, 1.0]];
    let mut synapse = GaussianSynapse::auto();
    let kernel = synapse.affinity(&states).unwrap();
    let report = check_preflight(&[0.0, 1.0, 2.0], &states, &kernel, 0.1);
    assert!(report.passed());
}

#[test]
fn memory_and_hebbian_work() {
    let root = std::env::temp_dir().join(format!("cosmic-rust-test-{}", std::process::id()));
    let path = root.join("memory.tsv");
    let _ = fs::remove_dir_all(&root);
    let mut memory = SemanticMemory::new(Some(&path), 128).unwrap();
    memory.store("the red guitar lives in the studio").unwrap();
    memory.store("bananas are yellow").unwrap();
    let recalled = memory.recall("where is the guitar?", 1);
    assert_eq!(recalled[0].0.text, "the red guitar lives in the studio");

    let mut hebbian = HebbianMemory::default();
    hebbian.learn("guitar music stage");
    assert!(!hebbian.associated_with("guitar", 2).is_empty());
    let _ = fs::remove_dir_all(root);
}

#[test]
fn event_bus_routes_events() {
    let seen = Arc::new(Mutex::new(0usize));
    let seen_clone = Arc::clone(&seen);
    let mut bus = EventBus::new();
    bus.subscribe("hello", move |_| {
        *seen_clone.lock().unwrap() += 1;
    });
    bus.emit(&Event::new("test", "hello"));
    assert_eq!(*seen.lock().unwrap(), 1);
}

#[test]
fn lorenz_moves() {
    let mut lorenz = Lorenz::default();
    let before = (lorenz.x, lorenz.y, lorenz.z);
    let after = lorenz.step(0.01).unwrap();
    assert_ne!(before, after);
}

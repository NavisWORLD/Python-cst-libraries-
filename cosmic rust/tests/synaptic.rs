use cosmic_rust::SynapticFunction;

fn close(a: f64, b: f64) -> bool {
    (a - b).abs() < 1e-12
}

#[test]
fn conformance_vector() {
    let function = SynapticFunction::new(0.75, 0.35).unwrap();
    let affinity = function
        .affinity(&[0.0, 1.0, -1.0, 0.5], &[0.5, 0.5, -0.5, 1.0])
        .unwrap();
    assert!(close(affinity, 0.41111229050718745));
    assert!(close(
        function.blend(0.8, affinity, None).unwrap(),
        0.6638893016775156
    ));
    let out = function
        .step(
            &[0.1, -0.2, 0.3, -0.4],
            &[1.0, -0.5, 0.25, -1.0],
            0.92,
            1.2,
            0.5,
        )
        .unwrap();
    assert!(close(out[0], 0.13323507494835604));
}

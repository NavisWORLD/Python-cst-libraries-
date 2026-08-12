use cosmic_rust::{CosmicRuntime, GaussianSynapse};

fn main() -> Result<(), String> {
    let mut runtime = CosmicRuntime::local(".cosmic-rust-demo")?;
    let reply = runtime.respond("music follows rhythm")?;
    println!("{reply}");

    let states = vec![vec![0.0, 0.0], vec![1.0, 0.5], vec![0.2, 1.0]];
    let diagnostics = GaussianSynapse::auto().diagnostics(&states)?;
    println!("kernel bandwidth={}", diagnostics.bandwidth);
    Ok(())
}

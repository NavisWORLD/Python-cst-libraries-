use cosmic_rust::SynapticFunction;
fn close(a:f64,b:f64)->bool{(a-b).abs()<1e-12}
#[test]fn conformance_vector(){let f=SynapticFunction::new(.75,.35).unwrap();let h=f.affinity(&[0.,1.,-1.,.5],&[.5,.5,-.5,1.]).unwrap();assert!(close(h,.41111229050718745));assert!(close(f.blend(.8,h,None).unwrap(),.6638893016775156));let o=f.step(&[.1,-.2,.3,-.4],&[1.,-.5,.25,-1.],.92,1.2,.5).unwrap();assert!(close(o[0],.13323507494835604));}

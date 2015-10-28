# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)

Gem::Specification.new do |spec|
  spec.name          = "GraphEditor"
  spec.version       = '1.0'
  spec.authors       = ["Michael Fürst"]
  spec.email         = ["penguinmenac3@gmail.com"]
  spec.summary       = %q{A graph editor to create and edit graphs for graph programming.}
  spec.description   = %q{A graph editor to create and edit graphs for graph programming. See github https://github.com/penguinmenac3/GraphProgramming}
  spec.homepage      = "https://github.com/penguinmenac3/GraphProgramming"
  spec.license       = "GNU GENERAL PUBLIC LICENSE"

  spec.files         = ['lib/grapheditor.rb']
  spec.executables   = ['bin/app.rb']
  spec.test_files    = ['tests/test_grapheditor.rb']
  spec.require_paths = ["lib"]
end
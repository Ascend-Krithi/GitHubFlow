package com.dsg.app.runner;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
        features = "src/androidTest/assets/features",
        glue = {"com.dsg.app.steps", "com.dsg.app.hooks"},
        plugin = {"pretty"}
)
public class TestRunner {
    // Configures Cucumber test execution
}

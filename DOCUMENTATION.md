# DSG Mobile Test Automation

## Build & Run Instructions

### Build
- ./gradlew assembleAndroidTest

### Run Tests
- ./gradlew connectedDebugAndroidTest

### Runner Arguments (Override Credentials)
- ./gradlew connectedDebugAndroidTest -Pandroid.testInstrumentationRunnerArguments.username=myuser -Pandroid.testInstrumentationRunnerArguments.password=mypass

### Troubleshooting
- Ensure emulator/device is running
- Disable animations on device
- Verify Espresso Idling Resources are registered
- Check for resource ID mismatches (replace TODOs with actual IDs)

## Usage Guidelines
- Each Gherkin step maps 1:1 to a Java step definition
- Page Objects encapsulate UI logic, no assertions
- Use WaitUtils for explicit waits, avoid Thread.sleep()
- Credentials are read via InstrumentationRegistry.getArguments()
- PermissionUtils handles location and notification permissions

## Maintenance
- Update resource IDs as UI evolves
- Add new Page Objects and utils as features grow
- Review and update Gradle dependencies periodically

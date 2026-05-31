# Progression RFC

## Decision

Progression hierarchy:

1. Car build is primary.
2. Driver skill is passive and achievement/XP based.
3. Team management arrives later as support.

This keeps the game about building and driving an underdog machine instead of
becoming a spreadsheet before the racing feels good.

## Car Build

Primary upgrade categories:

- Tires: grip, wear, surface behavior.
- Engine: acceleration, top speed, heat.
- Brakes: braking force, fade resistance, control.
- Gearbox: acceleration curve and top speed bias.
- Aerodynamics: high-speed stability, corner grip, drag.
- Weight: acceleration, braking, collision response.
- Cooling: endurance consistency.
- Durability: damage tolerance and repair cost.

Every upgrade should have a tradeoff or context.

Examples:

- Soft tires: high grip, high wear.
- Cheap turbo: strong acceleration, more heat.
- Light body: faster acceleration, weaker durability.
- High aero: better fast corners, more drag.

## Driver Skill

Driver growth should be passive achievement-based.

Good unlock triggers:

- Complete clean laps.
- Hit consistent lap times.
- Brake early for corners.
- Win with low damage.
- Finish endurance events with tire life remaining.
- Recover from drift without spinning.

Possible passive skills:

- Smoother throttle: small traction help.
- Better braking focus: slightly reduced lockup risk.
- Racecraft: minor reputation gain from clean wins.
- Endurance mindset: reduced tire wear in long events.

Driver skills should support mastery, not replace player skill.

## Resources

Early resources:

- Money: common upgrade currency.
- Reputation: unlocks events, sponsors, and license chances.
- Parts: optional crafting/discount resource.
- License progress: gates sanctioned tiers.
- Driver XP: passive skill progress.

Do not add too many currencies in CP3 or CP4. Start with money and reputation,
then add XP once driving behaviors exist.

## Street-To-Pro Advancement

Campaign gates should feel like social and mechanical advancement:

- Street events earn cash and reputation.
- Clean driving and results earn license interest.
- License tests unlock club racing.
- Club results unlock sponsors.
- Sponsors reduce costs or offer event goals.
- Pro tiers demand build specialization and consistency.

## Team Management Later

Team systems should wait until car build and driving feel are working.

Later team hooks:

- Crew improves repair speed/cost.
- Sponsors offer event objectives.
- Mechanics unlock upgrade branches.
- Logistics affect event availability.
- Engineer feedback explains tuning.

## Save Profile Shape

Future save data should track:

- Money.
- Reputation.
- Driver XP and passive skills.
- Owned vehicles.
- Installed parts.
- Unlocked events.
- Best lap times.
- License progress.
- Sponsor/team state later.

The save should store simulation/campaign data only, not Phaser scene objects.

## Test Strategy

Progression tests should verify:

- Race results grant money and reputation.
- Upgrade purchases change car stats.
- Driver XP unlocks passives from achievements.
- License gates block or allow events.
- Save/load preserves campaign progress.

float f_target(float psi_target)
{
    // forcelet parameter
    float lambda = 5.;

    return -lambda * sin(psi_target);
}

float f_obstacle(float ps_distance)
{
    // forcelet parameter
    float sigma = pi / 3;
    float beta_1 = 15.;
    float beta_2 = 10.;
    // [psi0, psi1, psi2, ...]
    float psi_obs[8] = [1.27, 0.77, 0., 5.21, 4.21, pi, 2.37, 1.87] - pi / 2;

    float lambda = beta_1*exp(-ps_distance / beta_2);

    return lambda *psi_obs *exp(-psi_obs ^ 2 / (2 * sigma ^ 2));
}

float* MovementAttractor(float psi_target)
{
    float v[2];
    // parameter
    float max_v = 6.28;
    float v_0 = 0.2 * max_v;

    // berechne forcelets
    float orientation_change = (f_target(psi_tar)) + sum(f_obstacle(ps_distance));
    orientation_change = min(max(orientation_change, -max_v), max_v);

    // beschränke änderung auf mögliche geschwindigkeiten
    if (abs(v_0 - orientation_change) > max_v || abs(v_0 + orientation_change) > max_v)
    {
        v[0] = sign(orientation_change) * max_v;
        v[1] = -vL;
    }
    else
    {
        v[0] = v_0 + orientation_change;
        v[1] = v_0 - orientation_change;
    }
    return v;
}
